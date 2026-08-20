from app.graph.state import ResumeState
from app.llm.client import ollama_client
from app.schemas.writer import ResumeWriterResult

SYSTEM_PROMPT = """
You are a professional resume optimization agent.

Your task is to improve a candidate's resume for a specific job
description while preserving factual accuracy.

You may:
- Improve wording.
- Improve clarity.
- Reorganize content.
- Strengthen action-oriented language.
- Highlight experience already present in the original resume.
- Improve alignment with relevant job-description terminology.
- Remove unnecessary repetition.
- Improve readability.
- Emphasize relevant technical skills already supported by the resume.

You MUST NOT:
- Invent skills.
- Invent employers.
- Invent projects.
- Invent certifications.
- Invent responsibilities.
- Invent technologies.
- Invent accomplishments.
- Invent numbers or measurable results.
- Claim experience with a missing ATS skill unless the original resume
  contains evidence supporting that skill.

IMPORTANT:

A keyword being listed as missing by the ATS analysis does NOT mean
you should automatically add that keyword.

Only add or emphasize a keyword when the original resume provides
reasonable factual evidence supporting it.

If an important keyword cannot safely be added, include it in
keywords_not_added.

Preserve important factual information including:
- employers
- job titles
- employment dates
- education
- certifications
- technical experience

Return a complete optimized resume.
"""

async def write_resume(
    state: ResumeState,
) -> ResumeWriterResult:

    print(">>> Running REAL Resume Writer using Ollama")

    original_resume = state["original_resume"]

    job_description = state["job_description"]

    profile_analysis = state[
        "profile_analysis"
    ]

    ats_analysis = state[
        "ats_analysis"
    ]

    target_role = state.get(
        "target_role"
    )

    review_result = state.get(
        "review_result"
    )

    revision_count = state.get(
        "revision_count",
        0,
    )

    review_feedback = ""

    if review_result is not None:

        review_feedback = f"""
PREVIOUS REVIEW FEEDBACK
========================

{review_result.model_dump_json(indent=2)}
"""

    user_prompt = f"""
TARGET ROLE
===========
{target_role or "Not provided"}


ORIGINAL RESUME
===============
{original_resume}


JOB DESCRIPTION
===============
{job_description}


PROFILE ANALYSIS
================
{profile_analysis.model_dump_json(indent=2)}


ATS ANALYSIS
============
{ats_analysis.model_dump_json(indent=2)}


CURRENT WRITER ATTEMPT
======================
{revision_count + 1}


{review_feedback}


TASK
====

Create an optimized version of the resume.

Focus on:

1. Improving alignment with the job description.
2. Emphasizing relevant experience already present in the resume.
3. Improving wording and readability.
4. Strengthening technical terminology where factually supported.
5. Reducing unnecessary repetition.
6. Preserving all important factual information.
7. Improving ATS-friendly wording.

Do not add unsupported skills or experience.

For every important ATS keyword you cannot safely add because the
original resume does not support it, include it in keywords_not_added.
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
        response_model=ResumeWriterResult,
    )