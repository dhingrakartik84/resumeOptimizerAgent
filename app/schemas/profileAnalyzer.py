# {
#   "years_of_experience": 15,
#   "identified_skills": [
#     "Java",
#     "Spring Boot",
#     "Kafka"
#   ],
#   "matched_skills": [
#     "Java",
#     "Spring Boot"
#   ],
#   "missing_skills": [
#     "Terraform"
#   ],
#   "strengths": [
#     "Microservices architecture"
#   ],
#   "gaps": [
#     "Cloud deployment experience is not clearly demonstrated"
#   ],
#   "skill_matches": [
#     {
#       "skill": "Java",
#       "required": true,
#       "present_in_resume": true,
#       "confidence": 0.98
#     }
#   ],
#   "experience_summary": "Senior backend engineer with strong Java and microservices experience."
# }


# Schema placeholder for profile analyzer
from pydantic import BaseModel, Field


class SkillMatch(BaseModel):
    skill: str
    required: bool = False
    present_in_resume: bool = False
    confidence: float = Field(ge=0.0, le=1.0)


class ProfileAnalysis(BaseModel):
    years_of_experience: int | None = None

    identified_skills: list[str] = Field(default_factory=list)

    matched_skills: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)

    strengths: list[str] = Field(default_factory=list)

    gaps: list[str] = Field(default_factory=list)

    skill_matches: list[SkillMatch] = Field(default_factory=list)

    experience_summary: str | None = None