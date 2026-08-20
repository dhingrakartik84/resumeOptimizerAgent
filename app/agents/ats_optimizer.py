from app.graph.state import ResumeState
from app.llm.client import ollama_client
from app.schemas.ats import (
    ATSAnalysis,
    ATSMetrics,
)

SYSTEM_PROMPT = """
You are an ATS resume analysis agent.

Analyze the candidate's resume against the supplied job description.

Evaluate:

1. Overall compatibility between resume and job description.
2. Required and preferred skill alignment.
3. Keyword alignment.
4. Experience relevance.
5. Readability.
6. Resume section completeness.
7. ATS-friendly formatting based only on the extracted text.
8. Missing important skills and keywords.
9. Concrete recommendations for improvement.

Rules:

- Never claim the candidate has a skill that is not supported by the resume.
- Do not invent experience, certifications, employers, or achievements.
- Scores must be between 0 and 100.
- compatibility_score represents your overall estimate of resume-to-job
  alignment. It is not a score from a specific commercial ATS product.
- formatting_score should only evaluate what can reasonably be inferred
  from the extracted resume text.
- If something cannot be determined, mention it in warnings.
"""

async def analyze_ats(
    state: ResumeState,
) -> ATSAnalysis:

    print(">>> Running REAL ATS Agent using Ollama")

    resume = state["original_resume"]
    job_description = state["job_description"]
    profile_analysis = state["profile_analysis"]

    user_prompt = f"""
CANDIDATE RESUME
================
{resume}

JOB DESCRIPTION
===============
{job_description}

PROFILE ANALYSIS
================
{profile_analysis.model_dump_json(indent=2)}

Analyze the resume for ATS compatibility.

Populate ATSMetrics by estimating:
- keyword match percentage
- required skill match percentage
- section completeness percentage
- matched and missing keywords
- matched and missing required skills
- detected and missing resume sections

Also evaluate:
- overall compatibility
- experience relevance
- readability
- formatting
- recommendations

Do not invent candidate experience or skills.
"""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    return await ollama_client.structured_chat(
        messages=messages,
        response_model=ATSAnalysis,
    )