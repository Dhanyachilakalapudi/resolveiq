from dataclasses import dataclass
from typing import Optional


@dataclass
class RuleResult:
    exception_type: str
    severity: str
    reason: str
    auto_resolution_allowed: bool


PRICE_TOLERANCE = 0.05
QUANTITY_TOLERANCE = 0.02


def evaluate_price_mismatch(
    expected: Optional[float],
    actual: Optional[float]
) -> Optional[RuleResult]:

    if expected is None or actual is None or expected == 0:
        return None

    difference_ratio = abs(actual - expected) / expected

    if difference_ratio > PRICE_TOLERANCE:
        severity = "HIGH" if difference_ratio >= 0.20 else "MEDIUM"

        return RuleResult(
            exception_type="PRICE_MISMATCH",
            severity=severity,
            reason=(
                f"Actual price {actual:.2f} differs from expected "
                f"price {expected:.2f} by "
                f"{difference_ratio * 100:.1f}%."
            ),
            auto_resolution_allowed=False
        )

    return None


def evaluate_quantity_mismatch(
    expected: Optional[float],
    actual: Optional[float]
) -> Optional[RuleResult]:

    if expected is None or actual is None or expected == 0:
        return None

    difference_ratio = abs(actual - expected) / expected

    if difference_ratio > QUANTITY_TOLERANCE:
        severity = "HIGH" if difference_ratio >= 0.10 else "MEDIUM"

        return RuleResult(
            exception_type="QUANTITY_MISMATCH",
            severity=severity,
            reason=(
                f"Actual quantity {actual:.0f} differs from expected "
                f"quantity {expected:.0f} by "
                f"{difference_ratio * 100:.1f}%."
            ),
            auto_resolution_allowed=False
        )

    return None


def evaluate_missing_po(
    expected: Optional[float],
    actual: Optional[float]
) -> Optional[RuleResult]:

    if expected is None and actual is not None:
        return RuleResult(
            exception_type="MISSING_PO",
            severity="HIGH",
            reason="No purchase order reference was found for this invoice.",
            auto_resolution_allowed=False
        )

    return None


def evaluate_duplicate(
    expected: Optional[float],
    actual: Optional[float]
) -> Optional[RuleResult]:

    if expected == 1 and actual >= 1:
        return RuleResult(
            exception_type="DUPLICATE_INVOICE",
            severity="MEDIUM",
            reason="A matching invoice record was detected.",
            auto_resolution_allowed=True
        )

    return None


def evaluate_tax_anomaly(
    expected: Optional[float],
    actual: Optional[float]
) -> Optional[RuleResult]:

    if expected is None or actual is None:
        return None

    if expected == 0:
        return None

    difference_ratio = abs(actual - expected) / expected

    if difference_ratio > PRICE_TOLERANCE:
        return RuleResult(
            exception_type="TAX_ANOMALY",
            severity="MEDIUM",
            reason=(
                f"Actual tax {actual:.2f} differs from expected tax "
                f"{expected:.2f} by {difference_ratio * 100:.1f}%."
            ),
            auto_resolution_allowed=False
        )

    return None


def evaluate_exception(
    exception_type: str,
    expected: Optional[float],
    actual: Optional[float]
) -> Optional[RuleResult]:

    evaluators = {
        "PRICE_MISMATCH": evaluate_price_mismatch,
        "QUANTITY_MISMATCH": evaluate_quantity_mismatch,
        "MISSING_PO": evaluate_missing_po,
        "DUPLICATE_INVOICE": evaluate_duplicate,
        "TAX_ANOMALY": evaluate_tax_anomaly,
    }

    evaluator = evaluators.get(exception_type)

    if evaluator is None:
        return None

    return evaluator(expected, actual)
