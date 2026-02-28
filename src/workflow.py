from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.agents.technical import technical_analysis_node
from src.agents.fundamental import fundamental_analysis_node
from src.agents.risk import risk_management_node
from src.db import log_evaluation

# 1. Define nodes

def reporting_node(state: AgentState) -> dict:
    """"""
    # Set default status if missing but not pass
    if "status" not in state or state["status"] in [None, "Pending"]:
        if state.get("technical_pass") is False or state.get("fundamental_pass") is False:
            state["status"] = "Rejected"
            if "rejection_reason" not in state or not state["rejection_reason"]:
                state["rejection_reason"] = "Failed Technical or Fundamental Analysis."
        else:
            state["status"] = "Pending_Risk"
            
    # Save the final state to DB
    log_evaluation(state)
    return state
    
def join_node(state: AgentState) -> dict:
    """"""
    # Dummy node to wait for parallel execution of technical and fundamental
    # LangGraph StateGraph handles reducer logic via updating TypedDict or just passing the accumulated state down.
    # We don't actually need to change state here, just serve as a synchronization point.
    return state

# 2. Define routing logic
def route_after_analysis(state: AgentState):
    """"""
    t_pass = state.get("technical_pass")
    f_pass = state.get("fundamental_pass")
    
    if t_pass and f_pass:
        return "risk_node"
    else:
        return "reporting_node"


# 3. Build Graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("technical", technical_analysis_node)
workflow.add_node("fundamental", fundamental_analysis_node)
workflow.add_node("join", join_node)
workflow.add_node("risk_node", risk_management_node)
workflow.add_node("reporting_node", reporting_node)

# Set parallel entry
workflow.add_edge(START, "technical")
workflow.add_edge(START, "fundamental")

# Both technical and fundamental point to join node
workflow.add_edge("technical", "join")
workflow.add_edge("fundamental", "join")

# Conditional edge from join node
workflow.add_conditional_edges(
    "join",
    route_after_analysis,
    {
        "risk_node": "risk_node",
        "reporting_node": "reporting_node"
    }
)

# After risk, go to reporting
workflow.add_edge("risk_node", "reporting_node")

# After reporting, end
workflow.add_edge("reporting_node", END)

# Compile the final graph
app = workflow.compile()

def analyze_ticker(ticker: str):
    """Convenience function to run a single ticker through the graph."""
    initial_state = {
        "current_ticker": ticker,
        "technical_pass": None,
        "technical_reasoning": None,
        "fundamental_pass": None,
        "fundamental_reasoning": None,
        "risk_metrics": None,
        "rejection_reason": None,
        "status": "Pending"
    }
    
    # Run graph
    result = app.invoke(initial_state)
    return result
