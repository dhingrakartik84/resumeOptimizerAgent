from fastapi import FastAPI

from app.api.routes.resumes import router as resumes_router

def create_app() -> FastAPI:
    app = FastAPI(title="Resume Agent System", 
                  description="Multi-agent AI system for resume optimization",
                  version="1.0.0")

    # Include the resumes router
    app.include_router(
        resumes_router,
        prefix="/api/v1",
        )

    @app.get("/health")
    async def health_check():
        return {"status": "UP"}

    return app

app = create_app()