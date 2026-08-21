from typing import Dict, Any

from .ai_service import generate_ai_analysis
from .confidence_gate import evaluate_confidence


def resolve_exception(exception) -> Dict[str, Any]:

    analysis = generate_ai_analysis(exception)

    confidence_result = evaluate_confidence(
        analysis["confidence"]
    )

    return {
        "exception_id": exception.exception_id,
        "exception_type": exception.exception_type,
        "severity": exception.severity,
        "analysis": analysis["analysis"],
        "recommended_action": analysis["recommended_action"],
        "confidence": analysis["confidence"],
        "decision": confidence_result.decision,
        "requires_human_review": confidence_result.requires_human_review,
        "confidence_reason": confidence_result.reason
    }
