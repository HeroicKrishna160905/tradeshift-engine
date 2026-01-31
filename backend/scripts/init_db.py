import sys
import os

# Ensure the parent directory is in the sys.path so we can import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base, engine, TradeLog

def init_db():
    print(f"🔌 Connecting to database using engine: {engine.url}")
    try:
        # Create all tables defined in the Base metadata
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully.")
        print("   - trade_logs")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

if __name__ == "__main__":
    init_db()
