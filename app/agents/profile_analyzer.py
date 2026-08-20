from app.graph.state import ResumeState
from app.llm.client import ollama_client
from app.schemas.profileAnalyzer import ProfileAnalysis, SkillMatch

SYSTEM_PROMPT = """
You are a resume profile analysis agent.

Your responsibility is to analyze a candidate's resume against
a target job description.

You must:

1. Identify skills explicitly supported by the resume.
2. Identify skills that match the job description.
3. Identify required skills that appear to be missing.
4. Identify candidate strengths.
5. Identify gaps relative to the job description.
6. Estimate years of professional experience only when reasonably
   supported by the resume.
7. Never invent skills, experience, certifications, employers,
   projects, or accomplishments.
8. If information cannot be determined, use null or an empty list.

For every skill match:
- required should indicate whether the job description requires it.
- present_in_resume should indicate whether evidence exists in the resume.
- confidence must be between 0 and 1.

Return only information supported by the supplied documents.
"""


async def analyze_profile(
    state: ResumeState,
) -> ProfileAnalysis:

    print(">>> Running Profile Analyzer Agent")

    print(">>> Running REAL Profile Analyzer using Ollama")

    resume = state["original_resume"]

    job_description = state["job_description"]

    target_role = state.get(
        "target_role"
    )

    user_prompt = f"""
        TARGET ROLE:
        {target_role or "Not provided"}

        CANDIDATE RESUME:
        -----------------
        {resume}

        JOB DESCRIPTION:
        ----------------
        {job_description}

        Analyze the candidate profile against the job description.
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

    result = await ollama_client.structured_chat(
        messages=messages,
        response_model=ProfileAnalysis,
    )

    return result