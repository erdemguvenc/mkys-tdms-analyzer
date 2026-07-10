from pathlib import Path

import pandas as pd

from analyzer.parsers.mkys_csv import MKYSCsvParser


def test_parser_reads_csv() -> None:
    parser = MKYSCsvParser()

    df = parser.parse(
        Path("sample_data/raw/giris_sorgulama.csv")
    )

    assert isinstance(df, pd.DataFrame)
    assert not df.empty