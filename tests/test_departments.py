import pytest
from sherkat_os.services.llm import llm_service
from sherkat_os.departments.market.schemas import MarketAnalysisReport
from sherkat_os.departments.market.nodes.analyst import market_analyst_node
from sherkat_os.departments.market.nodes.critic import market_critic_node

@pytest.mark.asyncio
async def test_llm_service_mock_structured_output():
    model = llm_service.get_model()
    structured = model.with_structured_output(MarketAnalysisReport)
    result = await structured.ainvoke("Generate test report for autonomous AI corporate simulation")
    assert isinstance(result, MarketAnalysisReport)
    assert result.overall_viability_score > 0
    assert len(result.personas) > 0

@pytest.mark.asyncio
async def test_market_analyst_node_execution():
    state = {
        "product_idea": "AI Autonomous Corporate Simulation Platform",
        "raw_research_data": {"tam_description": "10B USD"},
        "market_report": None,
        "critic_feedback": None,
        "retry_count": 0,
        "messages": []
    }
    result = await market_analyst_node(state)
    assert result["market_report"] is not None
    assert "market_size_description" in result["market_report"]

@pytest.mark.asyncio
async def test_market_critic_node_approval():
    state = {
        "market_report": {
            "market_size_description": "TAM 12B USD",
            "personas": [{"segment_name": "Devs", "pain_points": ["Slow manual setup"], "willingness_to_pay_rating": 8}],
            "competitor_landscape": [{"name": "CompA", "market_share_percentage": 20.0, "key_strengths": ["Brand"], "vulnerabilities": ["Legacy"]}],
            "industry_drivers": ["AI Agents"],
            "overall_viability_score": 8,
            "suggested_value_proposition": "Full agent orchestration"
        },
        "retry_count": 0,
        "messages": []
    }
    result = await market_critic_node(state)
    assert result["retry_count"] == 1
