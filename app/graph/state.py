#                     ResumeState
#                          │
#        ┌─────────────────┼─────────────────┐
#        │                 │                 │
#        ▼                 ▼                 ▼
#  Profile Analyzer    ATS Agent       Resume Writer
#        │                 │                 │
#        └─────────────────┼─────────────────┘
#                          │
#                          ▼
#                       Reviewer


from typing import TypedDict

from app.schemas.ats import ATSAnalysis, ATSMetrics
from app.schemas.profileAnalyzer import ProfileAnalysis
from app.schemas.reviewer import ReviewResult
from app.schemas.writer import ResumeWriterResult


class ResumeState(TypedDict, total=False):

    # Request identity
    request_id: str

    # Original inputs
    original_resume: str
    job_description: str
    target_role: str | None

    # Deterministic preprocessing / ATS data
    ats_metrics: ATSMetrics

    # Agent results
    profile_analysis: ProfileAnalysis
    ats_analysis: ATSAnalysis
    writer_result: ResumeWriterResult
    review_result: ReviewResult

    # Final output
    optimized_resume: str

    # Workflow controls
    approved: bool
    revision_count: int
    max_revisions: int

    # Operational information
    warnings: list[str]
    errors: list[str]