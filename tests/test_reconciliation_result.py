from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.consumption import ConsumptionMatch
from analyzer.reconciliation.duplicate import DuplicateMovement
from analyzer.reconciliation.result import ReconciliationResult


def create_movement(
    movement_type: MovementType = MovementType.ENTRY,
    amount: str = "100.00",
) -> Movement:
    """Testlerde kullanılacak örnek Movement oluşturur."""
    return Movement(
        source="MKYS",
        movement_type=movement_type,
        movement_date=date(2026, 1, 1),
        tif_no="TIF-001",
        voucher_no="FIS-001",
        document_no="DOC-001",
        invoice_no="INV-001",
        amount=Decimal(amount),
        description="Test hareketi",
        supplier="Test Tedarikçi",
        quantity=Decimal("1"),
    )


def test_reconciliation_result_defaults_are_empty():
    result = ReconciliationResult()

    assert result.matched == []
    assert result.missing_in_tdms == []
    assert result.missing_in_mkys == []
    assert result.amount_differences == []
    assert result.consumption_differences == []

    assert result.opening_matched == []
    assert result.opening_missing_in_tdms == []
    assert result.opening_missing_in_mkys == []

    assert result.scrap_matched == []
    assert result.scrap_missing_in_tdms == []
    assert result.scrap_missing_in_mkys == []
    assert result.scrap_amount_differences == []

    assert result.transfer_matched == []
    assert result.transfer_missing_in_tdms == []
    assert result.transfer_missing_in_mkys == []
    assert result.transfer_amount_differences == []


def test_reconciliation_result_stores_matched_movement():
    movement = create_movement()

    result = ReconciliationResult(
        matched=[movement],
    )

    assert len(result.matched) == 1
    assert result.matched[0] is movement


def test_reconciliation_result_stores_missing_movements():
    mkys_movement = create_movement(
        amount="150.00",
    )

    tdms_movement = create_movement(
        amount="200.00",
    )

    result = ReconciliationResult(
        missing_in_tdms=[mkys_movement],
        missing_in_mkys=[tdms_movement],
    )

    assert result.missing_in_tdms == [mkys_movement]
    assert result.missing_in_mkys == [tdms_movement]


def test_reconciliation_result_stores_opening_movements():
    movement = create_movement(
        amount="500.00",
    )

    result = ReconciliationResult(
        opening_matched=[movement],
        opening_missing_in_tdms=[movement],
        opening_missing_in_mkys=[movement],
    )

    assert result.opening_matched == [movement]
    assert result.opening_missing_in_tdms == [movement]
    assert result.opening_missing_in_mkys == [movement]


def test_reconciliation_result_stores_scrap_movements():
    movement = create_movement(
        movement_type=MovementType.SCRAP,
        amount="750.00",
    )

    result = ReconciliationResult(
        scrap_matched=[movement],
        scrap_missing_in_tdms=[movement],
        scrap_missing_in_mkys=[movement],
    )

    assert result.scrap_matched == [movement]
    assert result.scrap_missing_in_tdms == [movement]
    assert result.scrap_missing_in_mkys == [movement]


def test_reconciliation_result_stores_transfer_movements():
    movement = create_movement(
        movement_type=MovementType.TRANSFER,
        amount="300.00",
    )

    result = ReconciliationResult(
        transfer_matched=[movement],
        transfer_missing_in_tdms=[movement],
        transfer_missing_in_mkys=[movement],
    )

    assert result.transfer_matched == [movement]
    assert result.transfer_missing_in_tdms == [movement]
    assert result.transfer_missing_in_mkys == [movement]


def test_reconciliation_result_uses_independent_default_lists():
    first = ReconciliationResult()
    second = ReconciliationResult()

    movement = create_movement()

    first.matched.append(movement)

    assert first.matched == [movement]
    assert second.matched == []


def test_reconciliation_result_accepts_different_movement_types():
    entry = create_movement(
        movement_type=MovementType.ENTRY,
    )

    transfer = create_movement(
        movement_type=MovementType.TRANSFER,
    )

    scrap = create_movement(
        movement_type=MovementType.SCRAP,
    )

    result = ReconciliationResult(
        matched=[entry],
        transfer_matched=[transfer],
        scrap_matched=[scrap],
    )

    assert result.matched[0].movement_type is MovementType.ENTRY
    assert result.transfer_matched[0].movement_type is MovementType.TRANSFER
    assert result.scrap_matched[0].movement_type is MovementType.SCRAP


def test_reconciliation_result_stores_consumption_matches():
    match = ConsumptionMatch(
        year=2026,
        month=1,
        mkys_amount=Decimal("500.00"),
        tdms_amount=Decimal("500.00"),
    )

    result = ReconciliationResult(
        consumption_matched=[match],
    )

    assert result.consumption_matched == [match]
    assert len(result.consumption_matched) == 1

    stored_match = result.consumption_matched[0]

    assert stored_match.year == 2026
    assert stored_match.month == 1
    assert stored_match.mkys_amount == Decimal("500.00")
    assert stored_match.tdms_amount == Decimal("500.00")


def test_reconciliation_result_duplicate_movements_is_empty_by_default():
    result = ReconciliationResult()

    assert result.duplicate_movements == []


def make_movement(
    *,
    tif_no: str,
    movement_type: MovementType = MovementType.ENTRY,
    movement_date: date = date(2026, 1, 1),
    amount: str = "100.00",
) -> Movement:
    return Movement(
        source="test",
        movement_type=movement_type,
        movement_date=movement_date,
        tif_no=tif_no,
        voucher_no=None,
        document_no=None,
        invoice_no=None,
        amount=Decimal(amount),
        description="test movement",
        warehouse="",
        budget_type="",
        stock_code="",
        stock_name="",
        supplier="",
        quantity=Decimal("1"),
    )


def test_reconciliation_result_accepts_duplicate_movement():
    movement_1 = make_movement(
        tif_no="TIF-DUP-001",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 10),
        amount="100.00",
    )

    movement_2 = make_movement(
        tif_no="TIF-DUP-001",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 11),
        amount="200.00",
    )

    duplicate = DuplicateMovement(
        tif_no="TIF-DUP-001",
        movements=[movement_1, movement_2],
    )

    result = ReconciliationResult(
        duplicate_movements=[duplicate],
    )

    assert result.duplicate_movements == [duplicate]


def test_reconciliation_result_preserves_duplicate_details():
    movement_1 = make_movement(
        tif_no="TIF-DUP-002",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 2, 10),
        amount="100.00",
    )

    movement_2 = make_movement(
        tif_no="TIF-DUP-002",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 2, 11),
        amount="200.00",
    )

    duplicate = DuplicateMovement(
        tif_no="TIF-DUP-002",
        movements=[movement_1, movement_2],
    )

    result = ReconciliationResult(
        duplicate_movements=[duplicate],
    )

    stored_duplicate = result.duplicate_movements[0]

    assert stored_duplicate.tif_no == "TIF-DUP-002"
    assert stored_duplicate.movements == [movement_1, movement_2]
    assert len(stored_duplicate.movements) == 2
