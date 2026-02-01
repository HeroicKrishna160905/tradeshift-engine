# File: backend/app/oms.py

from datetime import datetime
from .models import TradeLog, SessionLocal


class OrderManager:
    def __init__(self):
        self.is_in_position = False
        self.entry_price = 0.0
        self.quantity = 0
        self.direction = 0  # 1: Long, -1: Short

        # 🔥 NEW STATE FOR ANALYTICS
        self.session_id = "default_session"
        self.entry_time = None
        self.last_trade_exit_time = None
        self.trade_counter = 0

    # =========================
    # BUY (open long)
    # =========================
    def buy(self, price: float, qty: int):
        """
        Executes a BUY (opens Long)
        """
        self.is_in_position = True
        self.entry_price = float(price)
        self.quantity = qty
        self.direction = 1

        # Track entry time
        self.entry_time = datetime.utcnow()

        print(f"🔵 OMS: BUY executed at {price} (Qty: {qty})")

    # =========================
    # SELL
    # =========================
    def sell(self, price: float, qty: int):
        """
        Executes a SELL.
        - If Long: closes trade and logs to DB
        - Else: opens Short
        """
        price = float(price)

        # =========================
        # CLOSE LONG → SAVE TRADE
        # =========================
        if self.is_in_position and self.direction == 1:

            pnl = (price - self.entry_price) * self.quantity * self.direction
            exit_time = datetime.utcnow()

            holding_time = (exit_time - self.entry_time).total_seconds()

            time_since_last = 0.0
            if self.last_trade_exit_time:
                time_since_last = (exit_time - self.last_trade_exit_time).total_seconds()

            self.trade_counter += 1

            print(f"🔴 OMS: CLOSED LONG at {price} | Realized PnL: {pnl:.2f}")

            # 🔥 SAVE TO DATABASE
            db = SessionLocal()

            trade = TradeLog(
                symbol="NIFTY",
                direction="LONG",
                entry_price=self.entry_price,
                exit_price=price,
                quantity=self.quantity,
                pnl=pnl,
                entry_time=self.entry_time,
                exit_time=exit_time,
                session_id=self.session_id,
                holding_time=holding_time,
                trade_number=self.trade_counter,
                stop_loss=None,
                take_profit=None,
                exit_reason="manual",
                time_since_last_trade=time_since_last
            )

            db.add(trade)
            db.commit()
            db.close()

            self.last_trade_exit_time = exit_time

            # Reset state
            self.is_in_position = False
            self.entry_price = 0.0
            self.quantity = 0
            self.direction = 0
            self.entry_time = None

            return pnl

        # =========================
        # OPEN SHORT (no logging yet)
        # =========================
        else:
            self.is_in_position = True
            self.entry_price = price
            self.quantity = qty
            self.direction = -1
            self.entry_time = datetime.utcnow()

            print(f"🔴 OMS: SHORT executed at {price} (Qty: {qty})")

            return 0.0

    # =========================
    # Unrealized PnL
    # =========================
    def calculate_pnl(self, current_price: float) -> float:
        if not self.is_in_position:
            return 0.0
        return (float(current_price) - self.entry_price) * self.quantity * self.direction
