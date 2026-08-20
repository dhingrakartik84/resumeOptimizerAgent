# FastAPI
#    ↓
# Workflow Service
#    ↓
# LangGraph
#    ↓
# Agents

import uuid

from app.graph.builder import resume_graph
from app.graph.state import ResumeState
from app.schemas.requests import ResumeOptimizationRequest
from app.schemas.responses import ResumeOptimizationResponse


async def optimize_resume(
    request: ResumeOptimizationRequest,
) -> ResumeOptimizationResponse:

    request_id = str(
        uuid.uuid4()
    )

    initial_state: ResumeState = {
        "request_id": request_id,

        "original_resume": request.resume,

        "job_description": (
            request.job_description
        ),

        "target_role": (
            request.target_role
        ),

        "revision_count": 0,

        "max_revisions": (
            request.max_revisions
        ),

        "approved": False,

        "warnings": [],

        "errors": [],
    }

    result = await resume_graph.ainvoke(
        initial_state
    )

    return ResumeOptimizationResponse(
        request_id=request_id,

        status="COMPLETED",

        optimized_resume=result.get(
            "optimized_resume"
        ),

        profile_analysis=result.get(
            "profile_analysis"
        ),

        ats_analysis=result.get(
            "ats_analysis"
        ),

        review_result=result.get(
            "review_result"
        ),

        revision_count=result.get(
            "revision_count",
            0,
        ),

        warnings=result.get(
            "warnings",
            [],
        ),
    )