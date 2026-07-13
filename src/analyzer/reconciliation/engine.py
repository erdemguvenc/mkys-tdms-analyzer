from __future__ import annotations

from analyzer.models.movement import Movement

from .matchers import EntryMatcher
from .result import ReconciliationResult


class ReconciliationEngine:

    def __init__(self) -> None:

        self._entry_matcher = EntryMatcher()

    def reconcile(
        self,
        mkys: list[Movement],
        tdms: list[Movement],
    ) -> ReconciliationResult:

        (
            matched,
            missing_tdms,
            missing_mkys,
        ) = self._entry_matcher.match(
            mkys,
            tdms,
        )

        return ReconciliationResult(
            matched=matched,
            missing_in_tdms=missing_tdms,
            missing_in_mkys=missing_mkys,
            amount_differences=[],
        )