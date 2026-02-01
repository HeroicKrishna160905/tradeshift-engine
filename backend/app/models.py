from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

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

    symbol = Column(String, index=True)
    direction = Column(String)

    entry_price = Column(Float)
    exit_price = Column(Float)
    quantity = Column(Integer)
    pnl = Column(Float)

    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, default=datetime.utcnow)

    # 🔥 NEW BEHAVIOR FIELDS (INSIDE CLASS)

    session_id = Column(String, index=True)

    holding_time = Column(Float)
    trade_number = Column(Integer)

    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)

    exit_reason = Column(String, nullable=True)

    time_since_last_trade = Column(Float, nullable=True)
