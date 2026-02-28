import yfinance as yf
import pandas as pd
from src.state import AgentState

# Hardware-coded constants for risk management
ACCOUNT_SIZE = 100000.0  # e.g., 1 lakh or 100k
MAX_RISK_PER_TRADE_PCT = 0.01  # 1% Account Risk

def calculate_atr(hist: pd.DataFrame, period=14) -> float:
    high_low = hist['High'] - hist['Low']
    high_close = (hist['High'] - hist['Close'].shift()).abs()
    low_close = (hist['Low'] - hist['Close'].shift()).abs()
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return float(atr.iloc[-1])

def risk_management_node(state: AgentState) -> dict:
    """"""
    # Only process if both technical and fundamental passed
    if not state.get("technical_pass") or not state.get("fundamental_pass"):
        return {
            "rejection_reason": "Failed upstream checks.",
            "status": "Rejected"
        }
        
    ticker_symbol = state["current_ticker"]
    ticker = yf.Ticker(ticker_symbol)
    
    try:
        # Need historical data to calculate ATR
        hist = ticker.history(period="1mo")
        if hist.empty or len(hist) < 14:
            return {
                "status": "Rejected",
                "rejection_reason": "Insufficient history for ATR calculation."
            }
            
        current_price = float(hist['Close'].iloc[-1])
        atr = calculate_atr(hist)
        
        # Stop loss logic (e.g., 2 ATR below entry)
        stop_loss_distance = 2 * atr
        stop_loss_price = current_price - stop_loss_distance
        
        # Position sizing logic
        risk_per_share = current_price - stop_loss_price
        max_capital_risk = ACCOUNT_SIZE * MAX_RISK_PER_TRADE_PCT
        
        if risk_per_share <= 0:
            return {
                "status": "Rejected",
                "rejection_reason": "Invalid risk per share calculated."
            }
            
        # Calculate shares and total exposure
        shares_to_buy = int(max_capital_risk // risk_per_share)
        total_position_size = shares_to_buy * current_price
        
        # Optional constraint: Max initial margin / position size (e.g., max 10% of portfolio in one position)
        if total_position_size > (ACCOUNT_SIZE * 0.10):
            # Cap the number of shares to 10% of portfolio
            shares_to_buy = int((ACCOUNT_SIZE * 0.10) // current_price)
            total_position_size = shares_to_buy * current_price
            
            if shares_to_buy == 0:
                 return {
                    "status": "Rejected",
                    "rejection_reason": "Price is too high to take even 1 share within risk limits."
                }
                
        metrics = {
            "entry_price": round(current_price, 2),
            "stop_loss_price": round(stop_loss_price, 2),
            "atr_14": round(atr, 2),
            "shares": shares_to_buy,
            "position_size": round(total_position_size, 2),
            "risk_amount": round(shares_to_buy * (current_price - stop_loss_price), 2)
        }
        
        return {
            "risk_metrics": metrics,
            "status": "Approved"
        }
        
    except Exception as e:
        return {
            "status": "Rejected",
            "rejection_reason": f"Risk Calculation Error: {str(e)}"
        }
