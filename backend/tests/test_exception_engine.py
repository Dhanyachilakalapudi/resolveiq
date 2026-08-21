from app.services.exception_engine import evaluate_exception


def test_price_mismatch():
    result = evaluate_exception(
        "PRICE_MISMATCH",
        100,
        125
    )

    assert result is not None
    assert result.exception_type == "PRICE_MISMATCH"
    assert result.severity == "HIGH"
    assert result.auto_resolution_allowed is False


def test_small_price_difference():
    result = evaluate_exception(
        "PRICE_MISMATCH",
        100,
        103
    )

    assert result is None


def test_quantity_mismatch():
    result = evaluate_exception(
        "QUANTITY_MISMATCH",
        50,
        65
    )

    assert result is not None
    assert result.exception_type == "QUANTITY_MISMATCH"


def test_missing_purchase_order():
    result = evaluate_exception(
        "MISSING_PO",
        None,
        4200
    )

    assert result is not None
    assert result.exception_type == "MISSING_PO"
    assert result.auto_resolution_allowed is False


def test_duplicate_invoice():
    result = evaluate_exception(
        "DUPLICATE_INVOICE",
        1,
        2
    )

    assert result is not None
    assert result.exception_type == "DUPLICATE_INVOICE"
    assert result.auto_resolution_allowed is True


def test_unknown_exception_type():
    result = evaluate_exception(
        "UNKNOWN",
        100,
        120
    )

    assert result is None
