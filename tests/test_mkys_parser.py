from __future__ import annotations

from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType


def test_parser_returns_movements(
    mkys_movements: list[Movement],
) -> None:
    assert isinstance(mkys_movements, list)
    assert len(mkys_movements) > 0
    assert isinstance(mkys_movements[0], Movement)


def test_first_movement_has_required_fields(
    mkys_movements: list[Movement],
) -> None:
    movement = mkys_movements[0]

    assert movement.source == "MKYS"
    assert movement.movement_type == MovementType.ENTRY

    assert movement.movement_date is not None

    assert movement.tif_no is not None
    assert isinstance(movement.tif_no, str)

    assert movement.amount >= Decimal("0")

    assert movement.stock_code is not None
    assert isinstance(movement.stock_code, str)

    assert movement.stock_name is not None
    assert isinstance(movement.stock_name, str)

    assert movement.quantity >= Decimal("0")


def test_parser_sets_warehouse_and_budget(
    mkys_movements: list[Movement],
) -> None:
    movement = mkys_movements[0]

    assert movement.warehouse is not None
    assert isinstance(movement.warehouse, str)

    assert movement.budget_type is not None
    assert isinstance(movement.budget_type, str)


def test_parser_sets_supplier(
    mkys_movements: list[Movement],
) -> None:
    movement = mkys_movements[0]

    assert movement.supplier is not None
    assert isinstance(movement.supplier, str)


def test_parser_sets_quantity(
    mkys_movements: list[Movement],
) -> None:
    movement = mkys_movements[0]

    assert movement.quantity >= Decimal("0")


def test_parser_sets_invoice_number(
    mkys_movements: list[Movement],
) -> None:
    movement = mkys_movements[0]

    assert movement.invoice_no is not None
    assert isinstance(movement.invoice_no, str)


def test_all_movements_are_entry(
    mkys_movements: list[Movement],
) -> None:
    assert all(
        movement.movement_type == MovementType.ENTRY for movement in mkys_movements
    )


def test_all_movements_have_dates(
    mkys_movements: list[Movement],
) -> None:
    assert all(movement.movement_date is not None for movement in mkys_movements)


def test_all_movements_have_amount(
    mkys_movements: list[Movement],
) -> None:
    assert all(movement.amount >= Decimal("0") for movement in mkys_movements)
