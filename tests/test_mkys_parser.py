from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.parsers.mkys_csv import MKYSCsvParser


SAMPLE_FILE = Path("sample_data/raw/giris_sorgulama.csv")


def test_parser_returns_movements() -> None:
    parser = MKYSCsvParser()

    movements = parser.parse(SAMPLE_FILE)

    assert isinstance(movements, list)
    assert len(movements) > 0
    assert isinstance(movements[0], Movement)


def test_first_movement_has_required_fields() -> None:
    parser = MKYSCsvParser()

    movement = parser.parse(SAMPLE_FILE)[0]

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


def test_parser_sets_warehouse_and_budget() -> None:
    parser = MKYSCsvParser()

    movement = parser.parse(SAMPLE_FILE)[0]

    assert movement.warehouse is not None
    assert isinstance(movement.warehouse, str)

    assert movement.budget_type is not None
    assert isinstance(movement.budget_type, str)


def test_parser_sets_supplier() -> None:
    parser = MKYSCsvParser()

    movement = parser.parse(SAMPLE_FILE)[0]

    assert movement.supplier is not None
    assert isinstance(movement.supplier, str)


def test_parser_sets_quantity() -> None:
    parser = MKYSCsvParser()

    movement = parser.parse(SAMPLE_FILE)[0]

    assert movement.quantity >= Decimal("0")


def test_parser_sets_invoice_number() -> None:
    parser = MKYSCsvParser()

    movement = parser.parse(SAMPLE_FILE)[0]

    assert movement.invoice_no is not None
    assert isinstance(movement.invoice_no, str)


def test_all_movements_are_entry() -> None:
    parser = MKYSCsvParser()

    movements = parser.parse(SAMPLE_FILE)

    assert all(
        movement.movement_type == MovementType.ENTRY
        for movement in movements
    )


def test_all_movements_have_dates() -> None:
    parser = MKYSCsvParser()

    movements = parser.parse(SAMPLE_FILE)

    assert all(
        movement.movement_date is not None
        for movement in movements
    )


def test_all_movements_have_amount() -> None:
    parser = MKYSCsvParser()

    movements = parser.parse(SAMPLE_FILE)

    assert all(
        movement.amount >= Decimal("0")
        for movement in movements
    )