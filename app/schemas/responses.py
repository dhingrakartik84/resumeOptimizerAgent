from pydantic import BaseModel, Field

from app.schemas.ats import ATSAnalysis
from app.schemas.profileAnalyzer import ProfileAnalysis
from app.schemas.reviewer import ReviewResult


class ResumeOptimizationResponse(BaseModel):
    request_id: str

    status: str

    optimized_resume: str | None = None

    profile_analysis: ProfileAnalysis | None = None

    ats_analysis: ATSAnalysis | None = None

    review_result: ReviewResult | None = None

    revision_count: int = 0

    warnings: list[str] = Field(default_factory=list)