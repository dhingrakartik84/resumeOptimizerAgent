# resumeOptimizerAgent

A simple agent to analyze and optimize resumes.

Quickstart

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt  # or `pip install .` if using pyproject
```

2. Run the development server:

```bash
uvicorn app.main:app --reload
```

Files

- `.env` — local environment overrides (not committed)
- `pyproject.toml` — project metadata and dependencies
- `Dockerfile` — container image
