import pytest
from sherkat_os.core.state import LinkageState
from sherkat_os.departments.market.schemas import MarketAnalysisReport, TargetAudiencePersona, CompetitorDetails, CriticFeedback
from sherkat_os.departments.product.schemas import ProductRequirementDocument, ProductFeature, UserStory
from sherkat_os.departments.tech.schemas import TechnicalBlueprint, SystemArchitecture, APIEndpoint
from sherkat_os.departments.finance.schemas import FinancialPlan, CostItem, PricingTier
from sherkat_os.departments.hr.schemas import HRStaffingPlan, HiredRole, RecruitmentMilestone
from sherkat_os.departments.legal.schemas import LegalAudit, ComplianceRisk, PrivacyRequirement

def test_linkage_state_initialization():
    state: LinkageState = {
        "product_idea": "AI Autonomous Corporate Simulation",
        "market_analysis": None,
        "prd": None,
        "tech_roadmap": None,
        "financial_model": None,
        "hr_plan": None,
        "legal_compliance": None,
        "messages": []
    }
    assert state["product_idea"] == "AI Autonomous Corporate Simulation"
    assert state["market_analysis"] is None

def test_market_analysis_schema():
    report = MarketAnalysisReport(
        market_size_description="Global Enterprise AI Automation $15B TAM",
        personas=[
            TargetAudiencePersona(segment_name="PMs", pain_points=["Coordination"], willingness_to_pay_rating=9)
        ],
        competitor_landscape=[
            CompetitorDetails(name="CorpX", market_share_percentage=25.0, key_strengths=["Sales"], vulnerabilities=["Tech debt"])
        ],
        industry_drivers=["Subgraphs", "LLMs"],
        overall_viability_score=9,
        suggested_value_proposition="Autonomous corporate execution"
    )
    assert report.overall_viability_score == 9
    assert len(report.personas) == 1

def test_critic_feedback_schema():
    feedback = CriticFeedback(
        is_approved=True,
        feedback="Market analysis passes enterprise quality bar.",
        score=9
    )
    assert feedback.is_approved is True
    assert feedback.score == 9
