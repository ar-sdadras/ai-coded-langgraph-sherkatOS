from pydantic import BaseModel, Field
from typing import List

class ComplianceRisk(BaseModel):
    area: str = Field(..., description="Regulatory area (e.g. GDPR, CCPA, HIPAA).")
    risk_level: str = Field(..., description="Risk severity (Critical, High, Medium, Low).")
    mitigation_strategy: str = Field(..., description="Technical or business solution to mitigate risk.")

class PrivacyRequirement(BaseModel):
    requirement_name: str = Field(..., description="Privacy requirement (e.g. Right to be forgotten).")
    implementation_details: str = Field(..., description="Technical integration needed.")

class LegalAudit(BaseModel):
    """
    Complex Pydantic schema representing the corporate compliance audit.
    """
    compliance_risks: List[ComplianceRisk] = Field(..., description="Identified legal risks and mitigations.")
    privacy_requirements: List[PrivacyRequirement] = Field(..., description="Explicit privacy rules for user data.")
    terms_of_service_guidelines: List[str] = Field(..., description="Key guidelines that must be in the TOS.")
    disclaimer_requirements: List[str] = Field(..., description="Disclaimers that must be presented to users.")
