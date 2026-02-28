import yfinance as yf
from src.state import AgentState

def fundamental_analysis_node(state: AgentState) -> dict:
    """"""
    ticker_symbol = state["current_ticker"]
    ticker = yf.Ticker(ticker_symbol)
    
    try:
        # yfinance can sometimes be missing data for small caps.
        info = ticker.info
        
        # Check basic fundamental health markers
        forward_eps = info.get("forwardEps")
        trailing_eps = info.get("trailingEps")
        revenue_growth = info.get("revenueGrowth")
        earnings_growth = info.get("earningsGrowth")
        
        reasons = []
        passed = True
        
        # We need at least trailing or forward EPS to be positive
        if trailing_eps is None and forward_eps is None:
            passed = False
            reasons.append("Missing EPS data.")
        else:
            if trailing_eps is not None and trailing_eps <= 0:
                if forward_eps is not None and forward_eps <= 0:
                    passed = False
                    reasons.append("Both trailing and forward EPS are negative.")
        
        # Prefer companies with positive revenue or earnings growth if available
        if revenue_growth is not None and revenue_growth < 0:
            reasons.append(f"Negative revenue growth ({revenue_growth:.2%}).")
            # We don't strictly fail on this immediately unless we want a very tight filter, 
            # but for a swing trade we might want at least some growth. Let's make it a strict rule.
            passed = False
            
        if earnings_growth is not None and earnings_growth < 0:
            reasons.append(f"Negative earnings growth ({earnings_growth:.2%}).")
            passed = False
            
        if passed:
            reasoning = "Fundamental metrics passed."
            if earnings_growth: reasoning += f" Earnings Growth: {earnings_growth:.2%}."
            if revenue_growth: reasoning += f" Revenue Growth: {revenue_growth:.2%}."
            return {
                "fundamental_pass": True,
                "fundamental_reasoning": reasoning
            }
        else:
            return {
                "fundamental_pass": False,
                "fundamental_reasoning": "Failed Fundamentals: " + " ".join(reasons)
            }
            
    except Exception as e:
        return {
            "fundamental_pass": False,
            "fundamental_reasoning": f"API or Calculation Error: {str(e)}"
        }
