from pathlib import Path

import pandas as pd

from analyzer.parsers.tdms_xls import TDMSXlsParser
from analyzer.constants.tdms_columns import REQUIRED_COLUMNS
from analyzer.constants import tdms_columns as COL


def test_parser_reads_xls() -> None:
    parser = TDMSXlsParser()

    df = parser.parse(
        Path("sample_data/raw/rapor.xls")
    )

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_print_first_rows() -> None:
    parser = TDMSXlsParser()

    df = parser.parse(
        Path("sample_data/raw/rapor.xls")
    )

    print(df.head(15).to_string())


def test_required_columns_exist():

    parser = TDMSXlsParser()

    df = parser.parse(
        Path("sample_data/raw/rapor.xls")
    )

    for column in REQUIRED_COLUMNS:
        assert column in df.columns


def test_debug_columns():
    parser = TDMSXlsParser()

    df = parser._read_xls(
        Path("sample_data/raw/rapor.xls")
    )

    print("\nREQUIRED_COLUMNS:")
    print(repr(COL.REQUIRED_COLUMNS))

    print("\nColumn check:")
    for c in COL.REQUIRED_COLUMNS:
        print(repr(c), c in df.columns)