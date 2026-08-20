from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.graph.nodes import (
    ats_optimizer_node,
    profile_analyzer_node,
    resume_writer_node,
    reviewer_node,
)
from app.graph.routes import route_after_review
from app.graph.state import ResumeState


def build_resume_graph():

    builder = StateGraph(
        ResumeState
    )

    #
    # Nodes
    #

    builder.add_node(
        "profile_analyzer",
        profile_analyzer_node,
    )

    builder.add_node(
        "ats_optimizer",
        ats_optimizer_node,
    )

    builder.add_node(
        "resume_writer",
        resume_writer_node,
    )

    builder.add_node(
        "reviewer",
        reviewer_node,
    )

    #
    # Normal flow
    #

    builder.add_edge(
        START,
        "profile_analyzer",
    )

    builder.add_edge(
        "profile_analyzer",
        "ats_optimizer",
    )

    builder.add_edge(
        "ats_optimizer",
        "resume_writer",
    )

    builder.add_edge(
        "resume_writer",
        "reviewer",
    )

    #
    # Reviewer decision
    #

    builder.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "rewrite": "resume_writer",
            "complete": END,
        },
    )

    return builder.compile()


resume_graph = build_resume_graph()