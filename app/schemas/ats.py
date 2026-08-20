
# Schema placeholders for ATS optimization results
from pydantic import BaseModel, Field


class ATSMetrics(BaseModel):
    keyword_match_percentage: float = Field(
        ge=0.0,
        le=100.0
    )

    required_skill_match_percentage: float = Field(
        ge=0.0,
        le=100.0
    )

    matched_keywords: list[str] = Field(default_factory=list)

    missing_keywords: list[str] = Field(default_factory=list)

    matched_required_skills: list[str] = Field(default_factory=list)

    missing_required_skills: list[str] = Field(default_factory=list)


class ATSAnalysis(BaseModel):
    compatibility_score: int = Field(
        ge=0,
        le=100
    )

    experience_relevance_score: int = Field(
        ge=0,
        le=100
    )

    readability_score: int = Field(
        ge=0,
        le=100
    )

    formatting_score: int = Field(
        ge=0,
        le=100
    )

    section_completeness_score: int = Field(
        ge=0,
        le=100
    )

    metrics: ATSMetrics

    recommendations: list[str] = Field(default_factory=list)

    formatting_issues: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)