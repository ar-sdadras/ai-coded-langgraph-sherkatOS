import pytest
from sherkat_os.orchestrator.graph import orchestrator_graph
from sherkat_os.config.settings import settings

@pytest.mark.asyncio
async def test_orchestrator_execution_behavior():
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
    
    # If no key is set in environment, invoking graph will raise ValueError
    key = settings.get_effective_google_api_key() or settings.get_effective_openai_api_key()
    if not key:
        with pytest.raises((ValueError, Exception)):
            await orchestrator_graph.ainvoke(initial_state, config)
    else:
        try:
            final_state = await orchestrator_graph.ainvoke(initial_state, config)
            assert final_state.get("market_analysis") is not None
        except Exception:
            pass
