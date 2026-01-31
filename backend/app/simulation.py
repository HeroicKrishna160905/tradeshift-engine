import numpy as np


class TickSynthesizer:
    """
    Generates realistic intra-candle tick data using the Brownian Bridge algorithm.
    
    The Brownian Bridge ensures the price path starts at 'open' and ends at 'close'
    while respecting the high/low boundaries of the candle.
    """
    
    def __init__(self, seed=None):
        """
        Initialize the TickSynthesizer.
        
        Args:
            seed: Optional random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
    
    def generate_ticks(self, open_price, high, low, close, num_ticks=60):
        """
        Generate tick prices using the Brownian Bridge formula.
        
        Formula: B(t) = Open + W(t) - (t/T) * (W(T) - (Close - Open))
        where W(t) is a Wiener process (cumulative sum of random normals).
        
        Args:
            open_price: Opening price of the candle
            high: High price of the candle
            low: Low price of the candle
            close: Closing price of the candle
            num_ticks: Number of ticks to generate (default: 60)
        
        Returns:
            List of tick prices (floats rounded to 2 decimals)
        """
        # Generate time steps
        T = num_ticks - 1  # Total time steps (0 to T)
        t = np.arange(num_ticks)
        
        # Generate Wiener process W(t)
        # Standard Brownian motion: cumulative sum of random normal increments
        dt = 1.0
        dW = np.random.normal(0, np.sqrt(dt), num_ticks)
        dW[0] = 0  # Start at zero
        W_t = np.cumsum(dW)
        
        # Apply Brownian Bridge formula
        # B(t) = Open + W(t) - (t/T) * (W(T) - (Close - Open))
        bridge = open_price + W_t - (t / T) * (W_t[-1] - (close - open_price))
        
        # Enforce high/low constraints using clamping
        bridge = np.minimum(bridge, high)  # Clamp to high
        bridge = np.maximum(bridge, low)   # Clamp to low
        
        # Ensure exact start and end values
        bridge[0] = open_price
        bridge[-1] = close
        
        # Convert to Python list with 2 decimal rounding
        ticks = [round(float(price), 2) for price in bridge]
        
        return ticks
