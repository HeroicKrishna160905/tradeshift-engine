import os
from minio import Minio
from sqlalchemy import create_engine, text
import re

# --- CONFIGURATION ---
MINIO_ENDPOINT = "localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "market-data"
DB_URL = "postgresql://user:password@localhost:5432/tradeshift"

def main():
    print("🚀 Starting Ingestor...")

    # 1. Connect to MinIO
    try:
        minio_client = Minio(MINIO_ENDPOINT, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
        if not minio_client.bucket_exists(BUCKET_NAME):
            print(f"❌ Error: Bucket '{BUCKET_NAME}' does not exist.")
            return
    except Exception as e:
        print(f"❌ Failed to connect to MinIO: {e}")
        return

    # 2. Connect to Database
    try:
        engine = create_engine(DB_URL)
        connection = engine.connect()
    except Exception as e:
        print(f"❌ Failed to connect to Database: {e}")
        return

    # 3. Scan & Insert
    try:
        objects = minio_client.list_objects(BUCKET_NAME, recursive=True)
        count = 0
        
        for obj in objects:
            file_path = obj.object_name  # e.g. "nifty50/NIFTY_50_1min.parquet"
            filename = file_path.split("/")[-1] 
            
            # --- NEW MATCHING LOGIC ---
            # Pattern A: Matches "NIFTY_2015.parquet"
            match_year = re.search(r"([A-Z0-9_]+)_(\d{4})\.parquet", filename)
            
            # Pattern B: Matches "NIFTY_50_1min.parquet" (Your current files)
            match_1min = re.search(r"^(.*)_1min\.parquet$", filename)

            symbol = None
            year = 2024 # Default year if not found

            if match_year:
                symbol = match_year.group(1)
                year = int(match_year.group(2))
            elif match_1min:
                symbol = match_1min.group(1)
                # Filename doesn't have year, so we default to 2024 or 0
                year = 2024 

            if symbol:
                print(f"   ✅ Found: {symbol} (Year {year}) -> {file_path}")
                
                query = text("""
                    INSERT INTO simulation_metadata (symbol, year, file_path)
                    VALUES (:symbol, :year, :path)
                    ON CONFLICT DO NOTHING;
                """)
                connection.execute(query, {"symbol": symbol, "year": year, "path": file_path})
                count += 1
            else:
                print(f"⚠️  Skipping: {filename}")

        connection.commit()
        print(f"\n🎉 Success! Cataloged {count} files.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()