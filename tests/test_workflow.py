from src.workflow import analyze_ticker

def test_workflow_rejection_on_invalid_ticker():
    # If we pass an invalid ticker or something with missing data, 
    # the workflow should gracefully reject it rather than crashing.
    result = analyze_ticker("INVALIDTICKER123")
    
    assert result["current_ticker"] == "INVALIDTICKER123"
    assert result["status"] == "Rejected"
    assert "technical_pass" in result
    assert "fundamental_pass" in result
    # It might fail either technical or fundamental or both, but the end result is Rejected
    
def test_workflow_structure():
    # Basic check to ensure the graph compiles and can be invoked
    try:
        from src.workflow import app
        assert app is not None
    except Exception as e:
        pytest.fail(f"Could not import or compile workflow: {e}")
