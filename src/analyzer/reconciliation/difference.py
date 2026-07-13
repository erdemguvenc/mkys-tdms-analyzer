from __future__ import annotations

from dataclasses import dataclass

from analyzer.models.movement import Movement


@dataclass(slots=True)
class AmountDifference:
    """
    Aynı hareketin tutar uyuşmazlığını temsil eder.
    """

    mkys: Movement

    tdms: Movement