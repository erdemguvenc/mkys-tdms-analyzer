from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.parsers.tdms_xls import TDMSXlsParser


SAMPLE_FILE = Path("sample_data/raw/rapor.xls")


def test_parser_returns_movements() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(SAMPLE_FILE)

    assert isinstance(movements, list)
    assert len(movements) > 0
    assert isinstance(movements[0], Movement)


def test_first_movement_has_required_fields() -> None:
    parser = TDMSXlsParser()

    movement = parser.parse(SAMPLE_FILE)[0]

    assert movement.source == "TDMS"
    assert movement.movement_type == MovementType.ENTRY

    assert movement.movement_date is not None

    assert movement.voucher_no is not None
    assert isinstance(movement.voucher_no, str)

    assert movement.tif_no is not None
    assert isinstance(movement.tif_no, str)

    assert movement.amount >= Decimal("0")


def test_parser_sets_supplier() -> None:
    parser = TDMSXlsParser()

    movement = parser.parse(SAMPLE_FILE)[0]

    assert movement.supplier is not None
    assert isinstance(movement.supplier, str)


def test_parser_sets_invoice_number() -> None:
    parser = TDMSXlsParser()

    movement = parser.parse(SAMPLE_FILE)[0]

    assert movement.invoice_no is not None
    assert isinstance(movement.invoice_no, str)


def test_parser_sets_description() -> None:
    parser = TDMSXlsParser()

    movement = parser.parse(SAMPLE_FILE)[0]

    assert movement.description is not None
    assert isinstance(movement.description, str)


def test_all_movements_are_entry() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(SAMPLE_FILE)

    assert all(
        movement.movement_type == MovementType.ENTRY
        for movement in movements
    )


def test_all_movements_have_positive_amount() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(SAMPLE_FILE)

    assert all(
        movement.amount >= Decimal("0")
        for movement in movements
    )


def test_all_movements_have_dates() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(SAMPLE_FILE)

    assert all(
        movement.movement_date is not None
        for movement in movements
    )


def test_all_movements_have_tif_number() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(SAMPLE_FILE)

    assert all(
        isinstance(movement.tif_no, str)
        for movement in movements
    )


def test_all_movements_have_voucher_number() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(SAMPLE_FILE)

    assert all(
        isinstance(movement.voucher_no, str)
        for movement in movements
    )