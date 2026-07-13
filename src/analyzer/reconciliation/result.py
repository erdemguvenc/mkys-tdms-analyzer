from __future__ import annotations

from dataclasses import dataclass, field

from analyzer.models.movement import Movement


@dataclass(slots=True)
class ReconciliationResult:
    """
    Uzlaştırma sonucunu tutar.
    """

    matched: list[Movement] = field(default_factory=list)

    missing_in_tdms: list[Movement] = field(default_factory=list)

    missing_in_mkys: list[Movement] = field(default_factory=list)

    amount_differences: list[Movement] = field(default_factory=list)