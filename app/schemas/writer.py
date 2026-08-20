# Schema placeholders for resume writer outputs
from pydantic import BaseModel, Field


class ResumeWriterResult(BaseModel):
    optimized_resume: str

    modifications: list[str] = Field(default_factory=list)

    keywords_added: list[str] = Field(default_factory=list)

    keywords_not_added: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)