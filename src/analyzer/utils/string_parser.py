from __future__ import annotations

import pandas as pd


def parse_string(value: object) -> str:
    """
    Ortak metin ayrıştırıcısı.
    """

    if pd.isna(value):
        return ""

    return str(value).strip()