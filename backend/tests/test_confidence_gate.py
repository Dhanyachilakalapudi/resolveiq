from app.services.confidence_gate import evaluate_confidence


def test_high_confidence():
    result = evaluate_confidence(0.95)

    assert result.decision == "AUTO-RESOLVE"
    assert result.auto_resolve is True
    assert result.requires_human_review is False
    assert result.threshold == 0.90


def test_low_confidence():
    result = evaluate_confidence(0.75)

    assert result.decision == "HUMAN REVIEW"
    assert result.auto_resolve is False
    assert result.requires_human_review is True


def test_threshold():
    result = evaluate_confidence(0.90)

    assert result.decision == "AUTO-RESOLVE"
    assert result.auto_resolve is True


def test_invalid_confidence():
    result = evaluate_confidence(None)

    assert result.decision == "HUMAN REVIEW"
    assert result.auto_resolve is False
    assert result.requires_human_review is True
