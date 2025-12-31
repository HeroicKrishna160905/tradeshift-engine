#!/usr/bin/env python3
"""
Data upload script for TradeShift
Uploads parquet files to MinIO and records metadata in TimescaleDB
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from minio import Minio
from minio.error import S3Error

# Add the parent directory to path for imports if needed
sys.path.append(str(Path(__file__).parent.parent))

# Configuration - using environment variables from docker-compose
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET_NAME = os.getenv("MINIO_BUCKET", "market-data")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tradeshift")

# Local path where parquet files are stored (mount this volume in docker-compose)
DATA_PATH = "/data"  # This will be mounted from host to container

def initialize_minio_client():
    """Initialize MinIO client"""
    # Remove protocol if present for MinIO client
    endpoint = MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
    return Minio(
        endpoint,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

def ensure_bucket_exists(client):
    """Create bucket if it doesn't exist"""
    try:
        if not client.bucket_exists(BUCKET_NAME):
            client.make_bucket(BUCKET_NAME)
            print(f"✅ Created bucket: {BUCKET_NAME}")
        else:
            print(f"✅ Bucket {BUCKET_NAME} already exists")
    except S3Error as e:
        print(f"❌ Error creating bucket: {e}")
        raise

def create_metadata_table(engine):
    """Create metadata table if it doesn't exist"""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS index_metadata (
                id SERIAL PRIMARY KEY,
                instrument VARCHAR(50) NOT NULL,
                interval VARCHAR(10) NOT NULL,
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                rows_count INTEGER NOT NULL,
                parquet_path VARCHAR(255) NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                bucket_name VARCHAR(100) NOT NULL,
                object_name VARCHAR(255) NOT NULL,
                UNIQUE(instrument, interval)
            );
        """))
        conn.commit()
    print("✅ Created/verified metadata table")

def upload_parquet_file(client, file_path, engine):
    """Upload a single parquet file and record metadata"""
    try:
        file_name = os.path.basename(file_path)
        
        # Extract instrument name from filename
        # Format: NIFTY_50_1min.parquet -> NIFTY_50
        instrument = file_name.replace("_1min.parquet", "")
        
        # Object name in MinIO
        object_name = f"indices/{file_name}"
        
        print(f"📤 Uploading {file_name}...")
        
        # Upload to MinIO
        client.fput_object(
            BUCKET_NAME,
            object_name,
            file_path,
            content_type="application/parquet"
        )
        
        # Read metadata from parquet file
        df = pd.read_parquet(file_path)
        
        # Insert metadata into database
        with engine.connect() as conn:
            # Delete existing entry if exists
            conn.execute(
                text("DELETE FROM index_metadata WHERE instrument = :instrument AND interval = '1min'"),
                {"instrument": instrument}
            )
            
            # Insert new entry
            conn.execute(text("""
                INSERT INTO index_metadata 
                (instrument, interval, start_date, end_date, rows_count, 
                 parquet_path, bucket_name, object_name)
                VALUES (:instrument, '1min', :start_date, :end_date, :rows_count,
                        :parquet_path, :bucket_name, :object_name)
            """), {
                'instrument': instrument,
                'start_date': df['date'].min(),
                'end_date': df['date'].max(),
                'rows_count': len(df),
                'parquet_path': object_name,
                'bucket_name': BUCKET_NAME,
                'object_name': object_name
            })
            conn.commit()
        
        print(f"✅ Uploaded: {instrument} ({len(df)} rows)")
        return True
        
    except Exception as e:
        print(f"❌ Error uploading {file_path}: {e}")
        return False

def main():
    """Main upload function"""
    print("🚀 Starting data upload process...")
    print("=" * 50)
    
    # Check if data directory exists
    if not os.path.exists(DATA_PATH):
        print(f"❌ Data directory not found: {DATA_PATH}")
        print("Please mount the data directory in docker-compose.yml")
        sys.exit(1)
    
    # Initialize clients
    minio_client = initialize_minio_client()
    db_engine = create_engine(DATABASE_URL)
    
    # Setup
    ensure_bucket_exists(minio_client)
    create_metadata_table(db_engine)
    
    # Find all parquet files
    parquet_files = []
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            if file.endswith('.parquet'):
                parquet_files.append(os.path.join(root, file))
    
    if not parquet_files:
        print("❌ No parquet files found in data directory")
        sys.exit(1)
    
    print(f"📁 Found {len(parquet_files)} parquet files")
    
    # Upload each file
    successful = 0
    failed = 0
    
    for file_path in parquet_files:
        if upload_parquet_file(minio_client, file_path, db_engine):
            successful += 1
        else:
            failed += 1
    
    print("=" * 50)
    print(f"📊 Upload Summary:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📂 Total: {len(parquet_files)}")
    
    if successful > 0:
        print("✨ Data upload completed successfully!")
    else:
        print("💥 No files were uploaded successfully")

if __name__ == "__main__":
    main()
