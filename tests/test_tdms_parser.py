from decimal import Decimal
from pathlib import Path

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.parsers.tdms_xls import TDMSXlsParser


def test_parser_returns_movements() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(
        Path("sample_data/raw/rapor.xls")
    )

    assert len(movements) > 0
    assert isinstance(movements[0], Movement)


def test_first_movement_has_required_fields() -> None:
    parser = TDMSXlsParser()

    movement = parser.parse(
        Path("sample_data/raw/rapor.xls")
    )[0]

    assert movement.source == "TDMS"
    assert movement.movement_type == MovementType.ENTRY

    assert movement.movement_date is not None

    assert movement.voucher_no != ""
    assert movement.description != ""

    assert isinstance(movement.amount, Decimal)


def test_all_movements_have_dates() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(
        Path("sample_data/raw/rapor.xls")
    )

    assert all(
        m.movement_date is not None
        for m in movements
    )


def test_all_movements_have_amount() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(
        Path("sample_data/raw/rapor.xls")
    )

    assert all(
        isinstance(m.amount, Decimal)
        for m in movements
    )


def test_all_movements_are_tdms() -> None:
    parser = TDMSXlsParser()

    movements = parser.parse(
        Path("sample_data/raw/rapor.xls")
    )

    assert all(
        m.source == "TDMS"
        for m in movements
    )