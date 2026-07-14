from __future__ import annotations

from analyzer.models.movement import Movement

from .consumption_matcher import ConsumptionMatcher
from .matchers import EntryMatcher
from .opening_matcher import OpeningMatcher
from .result import ReconciliationResult


class ReconciliationEngine:
    """
    MKYS ve TDMS hareketlerini uzlaştırır.
    """

    def __init__(self) -> None:

        self._entry_matcher = EntryMatcher()

        self._consumption_matcher = (
            ConsumptionMatcher()
        )

        self._opening_matcher = (
            OpeningMatcher()
        )

    def reconcile(
        self,
        mkys: list[Movement],
        tdms: list[Movement],
    ) -> ReconciliationResult:

        (
            matched,
            missing_tdms,
            missing_mkys,
            amount_differences,
        ) = self._entry_matcher.match(
            mkys,
            tdms,
        )

        consumption_differences = (
            self._consumption_matcher.match(
                mkys,
                tdms,
            )
        )

        (
            opening_matched,
            opening_missing_tdms,
            opening_missing_mkys,
        ) = self._opening_matcher.match(
            mkys,
            tdms,
        )

        return ReconciliationResult(
            matched=matched,
            missing_in_tdms=missing_tdms,
            missing_in_mkys=missing_mkys,
            amount_differences=amount_differences,
            consumption_differences=(
                consumption_differences
            ),
            opening_matched=(
                opening_matched
            ),
            opening_missing_in_tdms=(
                opening_missing_tdms
            ),
            opening_missing_in_mkys=(
                opening_missing_mkys
            ),
        )