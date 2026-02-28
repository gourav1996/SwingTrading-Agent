from typing import TypedDict, Optional

class AgentState(TypedDict):
    """
    Represents the state of the LangGraph multi-agent swing trading system 
    for a single ticker evaluated during the current run.
    """
    current_ticker: str
    
    # Technical Analysis
    technical_pass: Optional[bool]
    technical_reasoning: Optional[str]
    
    # Fundamental Analysis
    fundamental_pass: Optional[bool]
    fundamental_reasoning: Optional[str]
    
    # Risk Management
    risk_metrics: Optional[dict]
    
    # Final Outcome
    rejection_reason: Optional[str]
    status: Optional[str] # E.g., "Pending", "Approved", "Rejected"
