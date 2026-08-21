from typing import Dict, Any

from ..models import ExceptionRecord


def generate_ai_analysis(exception: ExceptionRecord) -> Dict[str, Any]:
    """
    Temporary deterministic AI-service interface.

    This provides a stable interface for the application while keeping
    the resolution logic explainable. The real LLM provider can be
    connected later without changing the API contract.
    """

    exception_type = exception.exception_type

    recommendations = {
        "PRICE_MISMATCH": (
            "Review the purchase order and vendor invoice. "
            "If the invoice price is incorrect, request a corrected invoice."
        ),
        "QUANTITY_MISMATCH": (
            "Compare the invoice quantity with the purchase order "
            "and receiving records before approving the invoice."
        ),
        "DUPLICATE_INVOICE": (
            "Verify whether this invoice is a duplicate before processing "
            "any payment."
        ),
        "TAX_ANOMALY": (
            "Verify the applicable tax rate and recalculate the invoice "
            "tax before approval."
        ),
        "MISSING_PO": (
            "Locate the corresponding purchase order or obtain the "
            "required procurement approval before processing."
        ),
    }

    recommendation = recommendations.get(
        exception_type,
        "Review the transaction manually before taking action."
    )

    if exception.severity == "HIGH":
        confidence = 0.91
    elif exception.severity == "MEDIUM":
        confidence = 0.82
    else:
        confidence = 0.70

    return {
        "exception_id": exception.exception_id,
        "analysis": (
            f"The transaction was identified as a "
            f"{exception_type.replace('_', ' ').lower()} "
            f"with {exception.severity.lower()} severity."
        ),
        "recommended_action": recommendation,
        "confidence": confidence,
        "requires_human_review": confidence < 0.90,
    }
