"""
전대상피질 (ACC) — 확신도 기반 라우팅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: 뇌간 분류 결과의 확신도에 따라 처리 깊이를 결정.
     90%+ → 바로 실행 (FAST)
     60~90% → 확인 후 실행 (BRAIN)
     60%- → 선택지 제시 (CLARIFY)
"""


def route_by_confidence(classification: dict) -> str:
    """확신도 기반 경로 결정.

    Returns:
        "FAST" | "BRAIN" | "CLARIFY"
    """
    complexity = classification.get("complexity", "복합")
    urgency = classification.get("urgency", "보통")

    if complexity == "단순" and urgency != "높음":
        return "FAST"

    routes = classification.get("route", [])
    if len(routes) >= 3 or complexity == "철학적":
        return "BRAIN"

    if urgency == "높음":
        return "FAST"

    return "BRAIN"
