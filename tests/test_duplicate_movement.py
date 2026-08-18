from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.duplicate import DuplicateMovement


def make_movement(
    *,
    tif_no: str | None,
    movement_type: MovementType,
    movement_date: date,
    amount: str,
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


def test_duplicate_movement_stores_tif_no():
    movement_1 = make_movement(
        tif_no="TIF-001",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 10),
        amount="100.00",
    )

    movement_2 = make_movement(
        tif_no="TIF-001",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 11),
        amount="200.00",
    )

    duplicate = DuplicateMovement(
        tif_no="TIF-001",
        movements=[movement_1, movement_2],
    )

    assert duplicate.tif_no == "TIF-001"


def test_duplicate_movement_stores_all_duplicate_movements():
    movement_1 = make_movement(
        tif_no="TIF-002",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 2, 10),
        amount="100.00",
    )

    movement_2 = make_movement(
        tif_no="TIF-002",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 2, 11),
        amount="200.00",
    )

    duplicate = DuplicateMovement(
        tif_no="TIF-002",
        movements=[movement_1, movement_2],
    )

    assert duplicate.movements == [movement_1, movement_2]
    assert len(duplicate.movements) == 2


def test_duplicate_movement_preserves_movement_order():
    movement_1 = make_movement(
        tif_no="TIF-003",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 3, 1),
        amount="100.00",
    )

    movement_2 = make_movement(
        tif_no="TIF-003",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 3, 2),
        amount="200.00",
    )

    duplicate = DuplicateMovement(
        tif_no="TIF-003",
        movements=[movement_1, movement_2],
    )

    assert duplicate.movements[0] is movement_1
    assert duplicate.movements[1] is movement_2


def test_duplicate_movement_is_frozen():
    movement = make_movement(
        tif_no="TIF-004",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 4, 1),
        amount="100.00",
    )

    duplicate = DuplicateMovement(
        tif_no="TIF-004",
        movements=[movement],
    )

    assert duplicate.tif_no == "TIF-004"

    try:
        setattr(duplicate, "tif_no", "TIF-999")
    except AttributeError:
        pass
    else:
        raise AssertionError("DuplicateMovement.tif_no değiştirilememelidir.")
