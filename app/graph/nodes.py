from app.agents.ats_optimizer import analyze_ats
from app.agents.profile_analyzer import analyze_profile
from app.agents.resume_writer import write_resume
from app.agents.reviewer import review_resume
from app.graph.state import ResumeState


async def profile_analyzer_node(
    state: ResumeState,
) -> dict:

    result = await analyze_profile(state)

    return {
        "profile_analysis": result,
    }


async def ats_optimizer_node(
    state: ResumeState,
) -> dict:

    result = await analyze_ats(state)

    return {
        "ats_analysis": result,
    }


async def resume_writer_node(
    state: ResumeState,
) -> dict:

    result = await write_resume(state)

    current_revision = state.get(
        "revision_count",
        0,
    )

    return {
        "writer_result": result,
        "optimized_resume": result.optimized_resume,
        "revision_count": current_revision + 1,
    }


async def reviewer_node(
    state: ResumeState,
) -> dict:

    result = await review_resume(state)

    return {
        "review_result": result,
        "approved": result.approved,
    }