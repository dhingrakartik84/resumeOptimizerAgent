from app.core.enums import IssueSeverity
from app.llm.client import ollama_client
from app.graph.state import ResumeState
from app.schemas.reviewer import (
    ReviewIssue,
    ReviewResult,
)


SYSTEM_PROMPT = """
You are a resume quality assurance and review agent.

Your responsibility is to review an optimized resume against:

1. The original resume.
2. The job description.
3. The profile analysis.
4. The ATS analysis.

The ORIGINAL RESUME is the primary factual source of truth.

You must check:

- Whether the optimized resume contains unsupported claims.
- Whether skills were added without evidence.
- Whether employers, dates, titles, certifications, projects,
  technologies, responsibilities, or accomplishments were invented.
- Whether important information from the original resume was lost.
- Whether the optimized resume is relevant to the job description.
- Whether ATS alignment has improved.
- Whether the wording is professional and readable.
- Whether the resume remains factually accurate.

APPROVAL RULES:

Approve the resume only if:

- There are no material unsupported claims.
- Factual accuracy is acceptable.
- The resume is clearly aligned with the target role.
- Readability is acceptable.
- No critical or high-severity issue requires correction.

If the resume should be revised:

- approved must be false.
- Include specific revision_instructions.
- Explain exactly what the Resume Writer should fix.
- Do not give vague feedback such as "make it better."

unsupported_claims must contain any statement or claim in the
optimized resume that cannot reasonably be supported by the
original resume.

Scores must be between 0 and 100.

Do not rewrite the resume yourself.
Your responsibility is review and quality control only.
"""


async def review_resume(
    state: ResumeState,
) -> ReviewResult:

    print(">>> Running REAL Reviewer using Ollama")

    original_resume = state[
        "original_resume"
    ]

    optimized_resume = state[
        "optimized_resume"
    ]

    job_description = state[
        "job_description"
    ]

    profile_analysis = state[
        "profile_analysis"
    ]

    ats_analysis = state[
        "ats_analysis"
    ]

    writer_result = state.get(
        "writer_result"
    )

    revision_count = state.get(
        "revision_count",
        0,
    )

    writer_metadata = ""

    if writer_result is not None:

        writer_metadata = (
            writer_result
            .model_dump_json(indent=2)
        )

    user_prompt = f"""
ORIGINAL RESUME
===============
{original_resume}


OPTIMIZED RESUME
================
{optimized_resume}


JOB DESCRIPTION
===============
{job_description}


PROFILE ANALYSIS
================
{profile_analysis.model_dump_json(indent=2)}


ATS ANALYSIS
============
{ats_analysis.model_dump_json(indent=2)}


WRITER METADATA
===============
{writer_metadata}


CURRENT REVISION
================
{revision_count}


TASK
====

Review the optimized resume.

Compare every important factual claim in the optimized resume
against the original resume.

Identify:

- unsupported experience
- unsupported skills
- invented technologies
- invented achievements
- invented metrics
- lost important information
- ATS alignment problems
- readability problems
- relevance problems

Return a structured ReviewResult.

Approve only when the resume is safe and sufficiently strong.

If you reject it, provide precise revision instructions for the
Resume Writer.
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
        response_model=ReviewResult,
    )