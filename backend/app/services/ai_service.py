from typing import Dict, Any


def generate_ai_analysis(exception) -> Dict[str, Any]:

    exception_type = exception.exception_type
    severity = exception.severity
    expected = exception.expected_value
    actual = exception.actual_value
    difference = exception.difference
    vendor = exception.vendor

    if exception_type == "PRICE_MISMATCH":

        analysis = (
            f"The invoice from {vendor} shows an actual value of "
            f"{actual}, while the expected value was {expected}. "
            f"This creates a difference of {difference}."
        )

        recommended_action = (
            "Verify the purchase order price and request "
            "vendor clarification before approving the invoice."
        )

        confidence = 0.94 if severity == "HIGH" else 0.91

    elif exception_type == "QUANTITY_MISMATCH":

        analysis = (
            f"The invoice quantity ({actual}) is different from "
            f"the expected quantity ({expected})."
        )

        recommended_action = (
            "Compare the invoice quantity with the purchase order "
            "and goods receipt before approval."
        )

        confidence = 0.93

    elif exception_type == "DUPLICATE_INVOICE":

        analysis = (
            "A similar invoice appears to already exist for this "
            "vendor. This may indicate a duplicate billing event."
        )

        recommended_action = (
            "Check the previous invoice and payment records before "
            "processing this invoice."
        )

        confidence = 0.96

    elif exception_type == "TAX_ANOMALY":

        analysis = (
            f"The expected tax value was {expected}, but the "
            f"invoice contains {actual}. The difference is {difference}."
        )

        recommended_action = (
            "Verify the applicable tax rate and recalculate the "
            "invoice tax before approval."
        )

        confidence = 0.92

    elif exception_type == "MISSING_PO":

        analysis = (
            f"The invoice from {vendor} cannot be matched to an "
            "existing purchase order."
        )

        recommended_action = (
            "Request or locate the purchase order before approving "
            "the invoice."
        )

        confidence = 0.78

    else:

        analysis = (
            f"The exception type is {exception_type} and requires "
            "additional investigation."
        )

        recommended_action = (
            "Send the exception to a human reviewer for investigation."
        )

        confidence = 0.70

    return {
        "analysis": analysis,
        "recommended_action": recommended_action,
        "confidence": confidence
    }
