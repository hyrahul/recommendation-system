def handle_clarification(
    language_code: str = "en",
) -> str:
    """
    Handles UNCLEAR intent.
    Returns clarification message as plain text.
    """

    if language_code == "ko":
        return (
            "어떤 도움을 원하시는지 조금 더 구체적으로 말씀해 주세요.\n"
            "예를 들어:\n"
            "- 강의 추천을 원하시나요?\n"
            "- 특정 개념에 대한 설명이 필요하신가요?"
        )

    return (
        "Could you please clarify what you are looking for?\n"
        "For example:\n"
        "- Are you looking for a course recommendation?\n"
        "- Do you want an explanation of a concept?"
    )
