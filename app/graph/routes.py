from typing import Literal

from app.graph.state import ResumeState


def route_after_review(
    state: ResumeState,
) -> Literal[
    "rewrite",
    "complete",
]:

    approved = state.get(
        "approved",
        False,
    )

    revision_count = state.get(
        "revision_count",
        0,
    )

    max_revisions = state.get(
        "max_revisions",
        2,
    )

    if approved:
        print(
            ">>> Reviewer approved resume"
        )

        return "complete"

    if revision_count >= max_revisions:
        print(
            ">>> Maximum revisions reached"
        )

        return "complete"

    print(
        ">>> Reviewer requested rewrite"
    )

    return "rewrite"