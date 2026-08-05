from __future__ import annotations

from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType


def test_parser_returns_movements(
    tdms_movements: list[Movement],
) -> None:
    assert isinstance(tdms_movements, list)
    assert len(tdms_movements) > 0
    assert isinstance(tdms_movements[0], Movement)


def test_first_movement_has_required_fields(
    tdms_movements: list[Movement],
) -> None:
    movement = tdms_movements[0]

    assert movement.source == "TDMS"
    assert movement.movement_type == MovementType.ENTRY

    assert movement.movement_date is not None

    assert movement.voucher_no is not None
    assert isinstance(movement.voucher_no, str)

    assert movement.tif_no is not None
    assert isinstance(movement.tif_no, str)

    assert movement.amount >= Decimal("0")


def test_parser_sets_supplier(
    tdms_movements: list[Movement],
) -> None:
    movement = tdms_movements[0]

    assert movement.supplier is not None
    assert isinstance(movement.supplier, str)


def test_parser_sets_invoice_number(
    tdms_movements: list[Movement],
) -> None:
    movement = tdms_movements[0]

    assert movement.invoice_no is not None
    assert isinstance(movement.invoice_no, str)


def test_parser_sets_description(
    tdms_movements: list[Movement],
) -> None:
    movement = tdms_movements[0]

    assert movement.description is not None
    assert isinstance(movement.description, str)


def test_all_movements_are_entry(
    tdms_movements: list[Movement],
) -> None:
    assert all(
        movement.movement_type == MovementType.ENTRY for movement in tdms_movements
    )


def test_all_movements_have_positive_amount(
    tdms_movements: list[Movement],
) -> None:
    assert all(movement.amount >= Decimal("0") for movement in tdms_movements)


def test_all_movements_have_dates(
    tdms_movements: list[Movement],
) -> None:
    assert all(movement.movement_date is not None for movement in tdms_movements)


def test_all_movements_have_tif_number(
    tdms_movements: list[Movement],
) -> None:
    assert all(isinstance(movement.tif_no, str) for movement in tdms_movements)


def test_all_movements_have_voucher_number(
    tdms_movements: list[Movement],
) -> None:
    assert all(isinstance(movement.voucher_no, str) for movement in tdms_movements)
