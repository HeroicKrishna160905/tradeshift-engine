# File: backend/app/oms.py

class OrderManager:
    def __init__(self):
        self.is_in_position = False
        self.entry_price = 0.0
        self.quantity = 0
        self.direction = 0  # 1: Long, -1: Short

    def buy(self, price: float, qty: int):
        """
        Executes a BUY. 
        Simplified logic: Always enters a Long position, overwriting state.
        """
        self.is_in_position = True
        self.entry_price = float(price)
        self.quantity = qty
        self.direction = 1
        print(f"🔵 OMS: BUY executed at {price} (Qty: {qty})")

    def sell(self, price: float, qty: int):
        """
        Executes a SELL.
        Logic: 
        - If Long: Closes the position.
        - If Not Long (Short or Warning): Opens a Short position.
        """
        price = float(price)
        if self.is_in_position and self.direction == 1:
            # Close Long
            pnl = (price - self.entry_price) * self.quantity * self.direction
            print(f"🔴 OMS: CLOSED LONG at {price} | Realized PnL: {pnl:.2f}")
            
            # Reset State
            self.is_in_position = False
            self.entry_price = 0.0
            self.quantity = 0
            self.direction = 0
            return pnl
        else:
            # Open Short
            self.is_in_position = True
            self.entry_price = price
            self.quantity = qty
            self.direction = -1
            print(f"🔴 OMS: SHORT executed at {price} (Qty: {qty})")
            return 0.0

    def calculate_pnl(self, current_price: float) -> float:
        """
        Calculates unrealized PnL based on current price.
        """
        if not self.is_in_position:
            return 0.0
        return (float(current_price) - self.entry_price) * self.quantity * self.direction