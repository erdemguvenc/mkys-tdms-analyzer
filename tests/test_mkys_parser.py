from pathlib import Path

from analyzer.models.movement import Movement
from analyzer.parsers.mkys_csv import MKYSCsvParser


def test_parser_returns_movements() -> None:
    parser = MKYSCsvParser()

    movements = parser.parse(
        Path("sample_data/raw/giris_sorgulama.csv")
    )

    assert isinstance(movements, list)
    assert len(movements) > 0
    assert isinstance(movements[0], Movement)


def test_first_movement_has_required_fields() -> None:
    parser = MKYSCsvParser()

    movement = parser.parse(
        Path("sample_data/raw/giris_sorgulama.csv")
    )[0]

    assert movement.tif_no
    assert movement.stock_code
    assert movement.stock_name
    assert movement.amount > 0


def test_first_row_date() -> None:
    parser = MKYSCsvParser()

    df = parser._read_csv(
        Path("sample_data/raw/giris_sorgulama.csv")
    )

    print(df.iloc[0]["Tarih"])