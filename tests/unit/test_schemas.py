from app.schemas.profileAnalyzer import ProfileAnalysis


def test_profile_analysis():

    result = ProfileAnalysis(
        years_of_experience=10,
        identified_skills=[
            "Java",
            "Spring Boot"
        ],
        matched_skills=[
            "Java"
        ],
        missing_skills=[
            "Kafka"
        ],
        strengths=[
            "Backend development"
        ],
        gaps=[
            "Kafka experience not found"
        ],
        experience_summary="Senior Java developer"
    )

    assert result.years_of_experience == 10

    assert "Java" in result.identified_skills

    assert "Kafka" in result.missing_skills