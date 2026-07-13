from __future__ import annotations

from dataclasses import dataclass, field

from analyzer.models.movement import Movement

from .difference import AmountDifference


@dataclass(slots=True)
class ReconciliationResult:
    """
    Uzlaştırma sonucu.
    """

    matched: list[Movement] = field(default_factory=list)

    missing_in_tdms: list[Movement] = field(default_factory=list)

    missing_in_mkys: list[Movement] = field(default_factory=list)

    amount_differences: list[AmountDifference] = field(
        default_factory=list
    )