from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Database Connection
# Using the service name 'db' as hostname for Docker internal networking
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/tradeshift")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TradeLog(Base):
    """
    Model representing a record of a completed trade.
    """
    __tablename__ = "trade_logs"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)      # e.g., 'NIFTY 50'
    direction = Column(String)               # 'LONG' or 'SHORT'
    entry_price = Column(Float)
    exit_price = Column(Float)
    quantity = Column(Integer)
    pnl = Column(Float)                      # Profit and Loss
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, default=datetime.utcnow)

