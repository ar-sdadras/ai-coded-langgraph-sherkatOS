import pytest
from sherkat_os.orchestrator.graph import orchestrator_graph

@pytest.mark.asyncio
async def test_orchestrator_full_simulation_run():
    initial_state = {
        "product_idea": "Test AI Corporate Orchestrator",
        "market_analysis": None,
        "prd": None,
        "tech_roadmap": None,
        "financial_model": None,
        "hr_plan": None,
        "legal_compliance": None,
        "messages": []
    }
    
    config = {
        "configurable": {
            "thread_id": "test_orchestrator_session_999"
        }
    }
    
    final_state = await orchestrator_graph.ainvoke(initial_state, config)
    
    assert final_state.get("market_analysis") is not None
    assert final_state.get("prd") is not None
    assert final_state.get("tech_roadmap") is not None
    assert final_state.get("financial_model") is not None
    assert final_state.get("hr_plan") is not None
    assert final_state.get("legal_compliance") is not None
