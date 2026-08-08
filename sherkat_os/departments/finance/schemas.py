from pydantic import BaseModel, Field
from typing import List, Optional

class CostItem(BaseModel):
    category: str = Field(..., description="Category of expense (e.g. Infrastructure, Labor).")
    estimated_monthly_cost: float = Field(..., description="Estimated cost per month in USD.")
    details: str = Field(..., description="Details and breakdown.")

class PricingTier(BaseModel):
    name: str = Field(..., description="Tier name (e.g. Developer, Enterprise).")
    price_usd: float = Field(..., description="Price per month/year.")
    included_features: List[str] = Field(..., description="Included scope of features.")

class FinancialPlan(BaseModel):
    """
    Complex Pydantic schema representing the corporate financial plan.
    """
    capital_requirement_usd: float = Field(..., description="Estimated capital needed to launch and run for 1 year.")
    monthly_burn_rate_usd: float = Field(..., description="Estimated operational burn rate.")
    operating_costs: List[CostItem] = Field(..., description="Detailed list of monthly operating expenses.")
    pricing_tiers: List[PricingTier] = Field(..., description="Available customer pricing plans.")
    estimated_payback_period_months: int = Field(..., description="Number of months to reach break-even.")

class CriticFeedback(BaseModel):
    is_approved: bool = Field(..., description="True if report passes quality bar, False otherwise.")
    feedback: str = Field(..., description="Detailed constructive feedback or approval summary.")
    score: int = Field(..., description="Quality score from 1-10.")
