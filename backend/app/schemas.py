from pydantic import BaseModel
from datetime import datetime

# Defines what a "Simulation Request" looks like
class SimulationStart(BaseModel):
    ticker: str       # e.g., "NIFTY50"
    start_date: str   # e.g., "2024-01-01"
    speed: int        # e.g., 1, 10, 100

# Defines what a single "Candle" looks like in the response
class CandleResponse(BaseModel):
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int