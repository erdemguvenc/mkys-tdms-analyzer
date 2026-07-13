from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from analyzer.models.movement import Movement


@dataclass(slots=True)
class AmountDifference:
    """
    Aynı hareketin tutar uyuşmazlığını temsil eder.
    """

    mkys: Movement
    tdms: Movement


@dataclass(slots=True)
class ConsumptionDifference:
    """
    Aylık tüketim toplamları arasındaki farkı temsil eder.
    """

    year: int

    month: int

    mkys_amount: Decimal

    tdms_amount: Decimal

    @property
    def difference(self) -> Decimal:
        return self.mkys_amount - self.tdms_amount