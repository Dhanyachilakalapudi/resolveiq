from app.services.confidence_gate import evaluate_confidence


def test_high_confidence():
    result = evaluate_confidence(0.95)

    assert result.decision == "RECOMMEND"
    assert result.requires_human_review is False


def test_low_confidence():
    result = evaluate_confidence(0.75)

    assert result.decision == "REVIEW"
    assert result.requires_human_review is True


def test_threshold():
    result = evaluate_confidence(0.90)

    assert result.decision == "RECOMMEND"
