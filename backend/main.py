
# Add to backend/main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import pandas as pd
from minio import Minio
import io

app = FastAPI()

# Database and MinIO clients
engine = create_engine("postgresql://user:password@db:5432/tradeshift")
minio_client = Minio("minio:9000", "minioadmin", "minioadmin", secure=False)

@app.get("/instruments")
def list_instruments():
    """Get all available instruments"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT instrument, start_date, end_date, rows_count FROM index_metadata"))
        return [dict(row) for row in result]

@app.get("/data/{instrument}")
def get_instrument_data(instrument: str, limit: int = 1000):
    """Get data for specific instrument"""
    # First check if instrument exists
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT object_name FROM index_metadata WHERE instrument = :instrument"),
            {"instrument": instrument}
        )
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Instrument not found")
        
        object_name = row[0]
    
    # Fetch from MinIO
    response = minio_client.get_object("market-data", object_name)
    df = pd.read_parquet(io.BytesIO(response.read()))
    
    # Convert to list of dicts
    return df.head(limit).to_dict(orient="records")

@app.get("/data/{instrument}/range")
def get_data_range(instrument: str, start: str, end: str):
    """Get data for specific date range"""
    # Similar implementation with date filtering
    pass

import os
import json
import random
import asyncio
import datetime
import uvicorn
import pandas as pd
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"🟢 Client Connected")

    try:
        data = await websocket.receive_text()
        message = json.loads(data)

        if message.get("command") == "START":
            speed = float(message.get("speed", 1))
            print(f"🚀 Streaming NIFTY Parquet at {speed}x")

            # Load the Parquet File
            file_path = "../data/NIFTY_50_1min.parquet"
            iterator = None
            using_real_data = False
            
            if os.path.exists(file_path):
                print(f"📂 Loaded: {file_path}")
                df = pd.read_parquet(file_path)
                # Normalize columns to lowercase for consistency
                df.columns = df.columns.str.lower()
                records = df.to_dict(orient="records")
                iterator = iter(records)
                using_real_data = True
            else:
                print("⚠️ Parquet not found. Using Random Fallback.")

            # STREAM LOOP
            while True:
                payload = {}
                
                if using_real_data:
                    try:
                        row = next(iterator)
                        
                        # Extract timestamps
                        ts = row.get('date') or row.get('datetime')
                        
                        # CRITICAL: Send full OHLC data
                        payload = {
                            "type": "CANDLE", # Changed from TICK to CANDLE
                            "data": {
                                "open": row.get('open'),
                                "high": row.get('high'),
                                "low": row.get('low'),
                                "close": row.get('close'),
                                "timestamp": str(ts),
                                "symbol": "NIFTY 50"
                            }
                        }
                    except StopIteration:
                        print("🏁 End of Data. Resetting...")
                        iterator = iter(records)
                        continue
                else:
                    # Random Fallback
                    price = 21500 + (random.random() - 0.5) * 10
                    payload = {
                        "type": "TICK",
                        "data": { "price": price, "timestamp": datetime.datetime.now().isoformat() }
                    }

                await websocket.send_json(payload)
                # Wait based on speed
                await asyncio.sleep(0.1 / max(speed, 0.1))

    except WebSocketDisconnect:
        print("🔴 Disconnected")
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

