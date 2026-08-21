from dataclasses import dataclass


@dataclass
class ConfidenceDecision:
    confidence: float
    decision: str
    requires_human_review: bool
    reason: str


AUTO_APPROVAL_THRESHOLD = 0.90


def evaluate_confidence(confidence: float) -> ConfidenceDecision:

    if confidence >= AUTO_APPROVAL_THRESHOLD:
        return ConfidenceDecision(
            confidence=confidence,
            decision="RECOMMEND",
            requires_human_review=False,
            reason="Confidence meets the configured threshold."
        )

    return ConfidenceDecision(
        confidence=confidence,
        decision="REVIEW",
        requires_human_review=True,
        reason="Confidence is below the configured threshold."
    )
