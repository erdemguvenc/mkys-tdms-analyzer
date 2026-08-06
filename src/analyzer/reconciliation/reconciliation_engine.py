from __future__ import annotations

from analyzer.models.movement import Movement
from analyzer.reconciliation.entry_matcher import EntryMatcher
from analyzer.reconciliation.result import ReconciliationResult


class ReconciliationEngine:
    """
    MKYS ve TDMS hareketlerinin uzlaştırılmasını yönetir.
    """

    def __init__(
        self,
    ) -> None:
        self._entry_matcher = EntryMatcher()

    def reconcile(
        self,
        mkys: list[Movement],
        tdms: list[Movement],
    ) -> ReconciliationResult:
        return self._entry_matcher.match(
            mkys,
            tdms,
        )
