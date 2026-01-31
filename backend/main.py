# File: backend/main.py

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import pandas as pd
from minio import Minio
import io
import os
import json
import asyncio
import datetime
from redis import Redis
from prometheus_fastapi_instrumentator import Instrumentator
from app.oms import OrderManager

# --- 1. ROBUST IMPORT FOR SIMULATION ---
try:
    from app.simulation import TickSynthesizer
    print("✅ Brownian Bridge Engine Loaded")
except ImportError:
    print("⚠️ Warning: simulation.py not found. Using Mock Fallback.")
    class TickSynthesizer:
        def generate_ticks(self, o, h, l, c, num_ticks=60):
            return [o] * num_ticks

app = FastAPI()

# Instrumentator (Monitoring)
Instrumentator().instrument(app).expose(app)

# --- 2. SECURITY (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. INFRASTRUCTURE CONNECTIONS ---
try:
    engine = create_engine("postgresql://user:password@db:5432/tradeshift")
except Exception as e:
    print(f"⚠️ DB Connection Warning: {e}")

try:
    minio_client = Minio("minio:9000", "minioadmin", "minioadmin", secure=False)
except Exception:
    pass

try:
    redis_client = Redis(host='tradeshift_redis', port=6379, decode_responses=True)
except Exception:
    print("⚠️ Redis not connected")

# --- 4. WEBSOCKET ENDPOINT ---
@app.websocket("/ws/ticker")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🟢 Client Connected")

    # Internal State
    is_running = False
    speed = 1.0
    synthesizer = TickSynthesizer()
    oms = OrderManager()
    last_tick_price = 21500.0  # Default value to prevent errors before stream starts
    
    # Data Source
    file_path = "data/NIFTY_50_1min.parquet"
    iterator = None
    using_real_data = False

    if os.path.exists(file_path):
        print(f"📂 Loaded: {file_path}")
        df = pd.read_parquet(file_path)
        df.columns = df.columns.str.lower()
        records = df.to_dict(orient="records")
        iterator = iter(records)
        using_real_data = True
    else:
        print("⚠️ Parquet not found. Using Synthetic Data Generation.")

    try:
        while True:
            # A. CHECK FOR COMMANDS (Non-blocking)
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.001)
                message = json.loads(data)
                command = message.get("command")
                
                if command == "START":
                    target_date = message.get("date")
                    speed = float(message.get("speed", 1.0))
                    
                    if using_real_data:
                        try:
                            # Date Logic
                            date_col = None
                            if 'date' in df.columns: date_col = 'date'
                            elif 'datetime' in df.columns: date_col = 'datetime'
                            
                            if not date_col:
                                await websocket.send_json({"type": "ERROR", "message": "Dataset has no date column"})
                                continue

                            # Filter DataFrame
                            temp_df = df.copy()
                            temp_df[date_col] = pd.to_datetime(temp_df[date_col])
                            
                            if not target_date:
                                first_date = temp_df[date_col].min().date()
                                target_date = str(first_date)
                            
                            target_dt = pd.to_datetime(target_date).date()
                            mask = temp_df[date_col].dt.date == target_dt
                            filtered_df = temp_df[mask]

                            if filtered_df.empty:
                                await websocket.send_json({"type": "ERROR", "message": f"No data found for date: {target_date}"})
                                continue

                            print(f"✅ Found {len(filtered_df)} records for {target_date}")
                            current_records = filtered_df.to_dict(orient="records")
                            iterator = iter(current_records)

                        except Exception as e:
                            print(f"❌ Date filtering error: {e}")
                            continue

                    is_running = True
                    print(f"▶️ Simulation Started (Speed: {speed}x)")
                
                # --- OMS INTEGRATION (The Fix) ---
                elif command == "BUY":
                    oms.buy(last_tick_price, qty=50)
                
                elif command == "SELL":
                    oms.sell(last_tick_price, qty=50)
                # ---------------------------------

            except asyncio.TimeoutError:
                pass # No command received, keep streaming

            # B. STREAM DATA (Only if running)
            if is_running:
                # 1. Get Next Candle
                if using_real_data:
                    try:
                        row = next(iterator)
                        open_p, high, low, close = row['open'], row['high'], row['low'], row['close']
                        base_time = pd.to_datetime(row.get('date') or row.get('datetime'))
                    except StopIteration:
                        print("🏁 End of Data. Restarting...")
                        iterator = iter(records)
                        continue
                else:
                    open_p, high, low, close = 21500, 21510, 21490, 21505
                    base_time = datetime.datetime.now()

                # 2. Generate 60 Micro-Ticks
                ticks = synthesizer.generate_ticks(open_p, high, low, close, num_ticks=60)

                # 3. Stream Loop (Batching)
                BATCH_SIZE = 10
                tick_batches = [ticks[i:i + BATCH_SIZE] for i in range(0, len(ticks), BATCH_SIZE)]
                
                for batch_index, batch_ticks in enumerate(tick_batches):
                    if not is_running: break 
                    
                    batch_data = []
                    for i, tick_price in enumerate(batch_ticks):
                        abs_index = (batch_index * BATCH_SIZE) + i
                        tick_time = base_time + datetime.timedelta(seconds=abs_index)
                        
                        # --- OMS UPDATE ---
                        last_tick_price = float(tick_price)
                        current_pnl = oms.calculate_pnl(last_tick_price)
                        # ------------------

                        batch_data.append({
                            "price": round(last_tick_price, 2),
                            "timestamp": tick_time.isoformat(),
                            "symbol": "NIFTY 50",
                            "pnl": round(current_pnl, 2)
                        })
                    
                    await websocket.send_json({"type": "BATCH", "data": batch_data})
                    await asyncio.sleep(0.1 / max(speed, 0.1))
            else:
                await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        print("🔴 Disconnected")
    except Exception as e:
        print(f"⚠️ Error: {e}")