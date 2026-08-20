from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from app.schemas.requests import ResumeOptimizationRequest
from app.schemas.responses import ResumeOptimizationResponse
from app.services.document_service import extract_text
from app.services.workflow_service import optimize_resume


router = APIRouter(
    prefix="/resumes",
    tags=["Resume"],
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post(
    "/optimize",
    response_model=ResumeOptimizationResponse,
)
async def optimize_resume_endpoint(
    resume: UploadFile = File(...),
    requirement: UploadFile = File(...),
    target_role: str | None = Form(default=None),
    max_revisions: int = Form(default=2),
):

    validate_upload(
        resume,
        "resume",
    )

    validate_upload(
        requirement,
        "requirement",
    )

    resume_bytes = await resume.read()

    requirement_bytes = await requirement.read()

    if len(resume_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Resume file is too large.",
        )

    if len(requirement_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Requirement file is too large.",
        )

    try:

        resume_text = extract_text(
            filename=resume.filename,
            content=resume_bytes,
        )

        requirement_text = extract_text(
            filename=requirement.filename,
            content=requirement_bytes,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    if not resume_text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in resume.",
        )

    if not requirement_text.strip():

        raise HTTPException(
            status_code=422,
            detail="No readable text found in requirement document.",
        )

    request = ResumeOptimizationRequest(
        resume=resume_text,
        job_description=requirement_text,
        target_role=target_role,
        max_revisions=max_revisions,
    )

    return await optimize_resume(request)



def validate_upload(
    file: UploadFile,
    label: str,
) -> None:

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail=f"{label} filename is missing.",
        )

    filename = file.filename.lower()

    if not any(
        filename.endswith(extension)
        for extension in ALLOWED_EXTENSIONS
    ):

        raise HTTPException(
            status_code=415,
            detail=(
                f"Unsupported {label} file type. "
                "Supported types are PDF, DOCX, and TXT."
            ),
        )