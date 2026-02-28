import pytest
import pandas as pd
from src.agents.risk import calculate_atr

def test_calculate_atr():
    # Create simple mock historical dataframe
    data = {
        'High': [10.5, 11.0, 10.8, 11.2, 11.5, 11.8, 12.0, 12.2, 12.5, 12.8, 13.0, 13.2, 13.5, 14.0],
        'Low':  [9.5, 10.0, 9.8, 10.2, 10.5, 10.8, 11.0, 11.2, 11.5, 11.8, 12.0, 12.2, 12.5, 13.0],
        'Close':[10.0, 10.5, 10.5, 11.0, 11.0, 11.5, 11.5, 12.0, 12.0, 12.5, 12.5, 13.0, 13.0, 13.5]
    }
    df = pd.DataFrame(data)
    
    atr = calculate_atr(df, period=14)
    # The true range for the first element is High-Low (1.0).
    # Subsequent elements depending on previous close.
    # We just ensure it returns a valid float greater than 0
    assert isinstance(atr, float)
    assert atr > 0
    
    # Manual check for a known small dataset
    data2 = {
        'High': [12.0, 12.0],
        'Low':  [10.0, 10.0],
        'Close':[11.0, 11.0]
    }
    df2 = pd.DataFrame(data2)
    atr2 = calculate_atr(df2, period=2)
    assert atr2 == 2.0  # (12-10) is range, average of 2.0 and 2.0 is 2.0
