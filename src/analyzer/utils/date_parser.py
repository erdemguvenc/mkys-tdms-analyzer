from __future__ import annotations

from datetime import date, datetime

import pandas as pd


_MONTHS = {
    "OCA": "01",
    "ŞUB": "02",
    "SUB": "02",
    "MAR": "03",
    "NİS": "04",
    "NIS": "04",
    "MAY": "05",
    "HAZ": "06",
    "TEM": "07",
    "AĞU": "08",
    "AGU": "08",
    "EYL": "09",
    "EKİ": "10",
    "EKI": "10",
    "KAS": "11",
    "ARA": "12",
}


def parse_date(value: object) -> date:
    """
    Ortak tarih ayrıştırıcısı.

    Desteklenen formatlar

    - 27.01.2026
    - 27/01/2026
    - 2026-01-27
    - 27-OCA-2026
    - 27-ŞUB-2026
    - 27-AĞU-2026
    """

    if pd.isna(value):
        raise ValueError("Tarih boş.")

    text = str(value).strip()

    if not text:
        raise ValueError("Tarih boş.")

    for fmt in (
        "%d.%m.%Y",
        "%d/%m/%Y",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(
                text,
                fmt,
            ).date()
        except ValueError:
            pass

    parts = text.upper().split("-")

    if len(parts) == 3:
        day, month, year = parts

        month = _MONTHS.get(month)

        if month is not None:
            return datetime.strptime(
                f"{day}.{month}.{year}",
                "%d.%m.%Y",
            ).date()

    raise ValueError(
        f"Desteklenmeyen tarih formatı: {text}"
    )