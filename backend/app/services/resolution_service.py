from typing import Dict, Any

from .ai_service import generate_ai_analysis
from .confidence_gate import evaluate_confidence


def resolve_exception(exception) -> Dict[str, Any]:

    try:
        analysis = generate_ai_analysis(exception)

        confidence = analysis.get("confidence")

        if confidence is None:
            confidence = 0.0

        confidence_result = evaluate_confidence(confidence)

        return {
            "exception_id": exception.exception_id,
            "exception_type": exception.exception_type,
            "severity": exception.severity,
            "analysis": analysis.get(
                "analysis",
                "AI analysis completed."
            ),
            "recommended_action": analysis.get(
                "recommended_action",
                "Human review is recommended."
            ),
            "confidence": confidence_result.confidence,
            "threshold": confidence_result.threshold,
            "decision": confidence_result.decision,
            "auto_resolve": confidence_result.auto_resolve,
            "requires_human_review": (
                confidence_result.requires_human_review
            ),
            "confidence_reason": confidence_result.reason,
        }

    except Exception:
        # Fail safely: never allow an AI failure to create
        # an autonomous resolution.
        return {
            "exception_id": exception.exception_id,
            "exception_type": exception.exception_type,
            "severity": exception.severity,
            "analysis": (
                "AI analysis is currently unavailable."
            ),
            "recommended_action": (
                "Review the exception manually before taking action."
            ),
            "confidence": 0.0,
            "threshold": 0.90,
            "decision": "HUMAN REVIEW",
            "auto_resolve": False,
            "requires_human_review": True,
            "confidence_reason": (
                "Automatic resolution is unavailable because "
                "AI analysis failed. Human review is required."
            ),
        }
