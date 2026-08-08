from pydantic import BaseModel, Field
from typing import List

class HiredRole(BaseModel):
    title: str = Field(..., description="Job title (e.g. Lead Agent Engineer).")
    department: str = Field(..., description="Department this role reports to.")
    years_experience_required: int = Field(..., description="Minimum years of experience.")
    core_skills: List[str] = Field(..., description="Key technical or soft skills.")
    target_salary_range_usd: str = Field(..., description="Annual base salary budget.")

class RecruitmentMilestone(BaseModel):
    milestone_name: str = Field(..., description="Name of milestone (e.g. Sourcing Backend Engineer).")
    estimated_weeks_to_fill: int = Field(..., description="Expected time to recruit.")
    priority: str = Field(..., description="Priority level (Critical, High, Medium, Low).")

class HRStaffingPlan(BaseModel):
    """
    Complex Pydantic schema representing the corporate recruitment plan.
    """
    total_headcount_target: int = Field(..., description="Total headcount desired for the MVP phase.")
    roles_list: List[HiredRole] = Field(..., description="Detailed requirements for every open role.")
    hiring_timeline_description: str = Field(..., description="Overall timeline breakdown.")
    recruitment_milestones: List[RecruitmentMilestone] = Field(..., description="Recruitment operational checkpoints.")
