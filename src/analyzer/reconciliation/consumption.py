from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class ConsumptionMatch:
    """Aylık tüketim uzlaştırmasında başarılı bir eşleşme."""

    year: int
    month: int
    mkys_amount: Decimal
    tdms_amount: Decimal
