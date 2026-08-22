from dataclasses import dataclass


@dataclass
class ConfidenceDecision:
    confidence: float
    threshold: float
    decision: str
    requires_human_review: bool
    auto_resolve: bool
    reason: str


# Backend source of truth for autonomous resolution.
AUTO_APPROVAL_THRESHOLD = 0.90


def evaluate_confidence(confidence: float) -> ConfidenceDecision:

    # Defensive handling for invalid AI confidence.
    if confidence is None or not isinstance(confidence, (int, float)):
        return ConfidenceDecision(
            confidence=0.0,
            threshold=AUTO_APPROVAL_THRESHOLD,
            decision="HUMAN REVIEW",
            requires_human_review=True,
            auto_resolve=False,
            reason=(
                "Confidence could not be determined. "
                "Human review is required."
            )
        )

    confidence = max(0.0, min(float(confidence), 1.0))

    if confidence >= AUTO_APPROVAL_THRESHOLD:
        return ConfidenceDecision(
            confidence=confidence,
            threshold=AUTO_APPROVAL_THRESHOLD,
            decision="AUTO-RESOLVE",
            requires_human_review=False,
            auto_resolve=True,
            reason=(
                "Confidence meets or exceeds the configured "
                "auto-resolution threshold."
            )
        )

    return ConfidenceDecision(
        confidence=confidence,
        threshold=AUTO_APPROVAL_THRESHOLD,
        decision="HUMAN REVIEW",
        requires_human_review=True,
        auto_resolve=False,
        reason=(
            "Confidence is below the configured auto-resolution "
            "threshold. Human review is required."
        )
    )
