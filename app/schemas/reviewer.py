# Schema placeholders for reviewer feedback
from pydantic import BaseModel, Field

from app.core.enums import IssueSeverity


class ReviewIssue(BaseModel):
    category: str
    description: str
    severity: IssueSeverity
    
class ReviewResult(BaseModel):
    approved: bool

    overall_score: int = Field(
        ge=0,
        le=100
    )

    factual_accuracy_score: int = Field(
        ge=0,
        le=100
    )

    ats_alignment_score: int = Field(
        ge=0,
        le=100
    )

    readability_score: int = Field(
        ge=0,
        le=100
    )

    relevance_score: int = Field(
        ge=0,
        le=100
    )

    issues: list[ReviewIssue] = Field(default_factory=list)

    revision_instructions: list[str] = Field(default_factory=list)

    unsupported_claims: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)