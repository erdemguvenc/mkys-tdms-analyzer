from __future__ import annotations

from typing import Any, cast

import pandas as pd


def parse_string(value: object) -> str:
    """
    Ortak metin ayrıştırıcısı.
    """

    if pd.isna(cast(Any, value)):
        return ""

    return str(value).strip()
