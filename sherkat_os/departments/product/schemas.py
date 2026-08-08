from pydantic import BaseModel, Field
from typing import List

class UserStory(BaseModel):
    as_a: str = Field(..., description="Role of user (e.g. As a Product Manager).")
    i_want_to: str = Field(..., description="Desired functionality (e.g. I want to launch simulations).")
    so_that: str = Field(..., description="Benefit/value (e.g. So that I can align teams).")
    acceptance_criteria: List[str] = Field(..., description="Detailed criteria to meet.")

class ProductFeature(BaseModel):
    name: str = Field(..., description="Feature name.")
    description: str = Field(..., description="Feature explanation.")
    priority: str = Field(..., description="Priority level (High, Medium, Low).")
    user_stories: List[UserStory] = Field(..., description="Associated user stories.")

class ProductRequirementDocument(BaseModel):
    """
    Complex Pydantic schema representing the complete PRD.
    """
    product_vision: str = Field(..., description="Core vision statement.")
    key_features: List[ProductFeature] = Field(..., description="Main features list.")
    scope_exclusions: List[str] = Field(..., description="Out of scope list.")
    success_metrics: List[str] = Field(..., description="KPIs to track success.")
    mvp_release_timeline: str = Field(..., description="Estimated release timeline description.")
