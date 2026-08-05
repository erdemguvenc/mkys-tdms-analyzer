from __future__ import annotations

from pathlib import Path

import pytest

from analyzer.models.movement import Movement
from analyzer.parsers.mkys_csv import MKYSCsvParser
from analyzer.parsers.tdms_xls import TDMSXlsParser

MKYS_SAMPLE = Path(
    "tests/data/mkys/mkys_sample.csv",
)

TDMS_SAMPLE = Path(
    "tests/data/tdms/tdms_sample.xlsx",
)


@pytest.fixture(scope="session")
def mkys_movements() -> list[Movement]:
    """
    Testlerde kullanılacak MKYS hareketleri.
    """

    parser = MKYSCsvParser()

    return parser.parse(
        MKYS_SAMPLE,
    )


@pytest.fixture(scope="session")
def tdms_movements() -> list[Movement]:
    """
    Testlerde kullanılacak TDMS hareketleri.
    """

    parser = TDMSXlsParser()

    return parser.parse(
        TDMS_SAMPLE,
    )
