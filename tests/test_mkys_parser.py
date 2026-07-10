from pathlib import Path

from analyzer.constants.mkys_columns import REQUIRED_COLUMNS
from analyzer.parsers.mkys_csv import MKYSCsvParser


def test_parser_removes_unnamed_columns() -> None:
    parser = MKYSCsvParser()

    df = parser.parse(
        Path("sample_data/raw/giris_sorgulama.csv")
    )

    assert all(
        not column.startswith("Unnamed")
        for column in df.columns
    )

def test_required_columns_exist() -> None:
    parser = MKYSCsvParser()

    df = parser.parse(
        Path("sample_data/raw/giris_sorgulama.csv")
    )

    for column in REQUIRED_COLUMNS:
        assert column in df.columns

def test_dataframe_is_not_empty() -> None:
    parser = MKYSCsvParser()

    df = parser.parse(
        Path("sample_data/raw/giris_sorgulama.csv")
    )

    assert len(df) > 0