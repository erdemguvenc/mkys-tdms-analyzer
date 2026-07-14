from __future__ import annotations

from decimal import Decimal
from decimal import InvalidOperation

import pandas as pd


def parse_decimal(value: object) -> Decimal:
    """
    Ortak sayısal değer ayrıştırıcısı.

    Desteklenen örnekler

    123
    123.45
    123,45
    1.234,56
    1,234.56
    None
    NaN
    ""
    """

    if pd.isna(value):
        return Decimal("0")

    text = str(value).strip()

    if not text:
        return Decimal("0")

    text = text.replace(" ", "")

    # Türkçe sayı biçimi
    # 1.234,56
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "")
            text = text.replace(",", ".")
        else:
            text = text.replace(",", "")

    # 123,45
    elif "," in text:
        text = text.replace(",", ".")

    try:
        return Decimal(text)

    except InvalidOperation:
        raise ValueError(
            f"Geçersiz sayısal değer: {value}"
        )