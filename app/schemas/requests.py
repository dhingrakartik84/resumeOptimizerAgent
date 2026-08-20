from pydantic import BaseModel, Field

class ResumeOptimizationRequest(BaseModel):
    resume: str = Field(min_length=50)
    job_description: str = Field(min_length=20)
    target_role: str | None = None
    max_revisions: int = Field(default = 2, ge=0, le=3)