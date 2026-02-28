import yfinance as yf
import pandas as pd
from src.state import AgentState

def technical_analysis_node(state: AgentState) -> dict:
    """"""
    ticker_symbol = state["current_ticker"]
    ticker = yf.Ticker(ticker_symbol)
    
    try:
        # Fetch 1 year of historical data to ensure we have enough for 200 SMA
        hist = ticker.history(period="1y")
        
        if hist.empty or len(hist) < 200:
            return {
                "technical_pass": False,
                "technical_reasoning": "Insufficient trading history (need at least 200 days)."
            }
        
        # Calculate SMAs
        hist['SMA50'] = hist['Close'].rolling(window=50).mean()
        hist['SMA150'] = hist['Close'].rolling(window=150).mean()
        hist['SMA200'] = hist['Close'].rolling(window=200).mean()
        
        current_data = hist.iloc[-1]
        current_price = current_data['Close']
        sma50 = current_data['SMA50']
        sma150 = current_data['SMA150']
        sma200 = current_data['SMA200']
        
        # 52-week high/low
        high_52 = hist['High'].max()
        low_52 = hist['Low'].min()
        
        # Basic Mark Minervini Trend Template conditions:
        # 1. Current Price > 50, 150, and 200 SMA
        # 2. 50 SMA > 150 SMA > 200 SMA
        # 3. 200 SMA is trending up for at least 1 month (approximate here)
        # 4. Current price is within 25% of 52-week high
        # 5. Current price is at least 30% above 52-week low
        
        cond1 = current_price > sma50 and current_price > sma150 and current_price > sma200
        cond2 = sma50 > sma150 and sma150 > sma200
        cond4 = current_price >= (high_52 * 0.75)
        cond5 = current_price >= (low_52 * 1.30)
        
        if cond1 and cond2 and cond4 and cond5:
            reasoning = f"Price ({current_price:.2f}) meets Minervini Trend Template. SMA50={sma50:.2f}, SMA150={sma150:.2f}, SMA200={sma200:.2f}."
            return {
                "technical_pass": True,
                "technical_reasoning": reasoning
            }
        else:
            reasons = []
            if not cond1: reasons.append("Price not above all SMAs.")
            if not cond2: reasons.append("SMAs not properly stacked (50 > 150 > 200).")
            if not cond4: reasons.append("Price not within 25% of 52-week high.")
            if not cond5: reasons.append("Price not 30% above 52-week low.")
            
            return {
                "technical_pass": False,
                "technical_reasoning": "Failed Minervini Template: " + " ".join(reasons)
            }
            
    except Exception as e:
        return {
            "technical_pass": False,
            "technical_reasoning": f"API or Calculation Error: {str(e)}"
        }
