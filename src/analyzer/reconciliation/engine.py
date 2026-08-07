from __future__ import annotations

from analyzer.models.movement import Movement
from analyzer.reconciliation.consumption_matcher import ConsumptionMatcher
from analyzer.reconciliation.entry_matcher import EntryMatcher
from analyzer.reconciliation.opening_matcher import OpeningMatcher
from analyzer.reconciliation.result import ReconciliationResult
from analyzer.reconciliation.transfer_matcher import TransferMatcher


class ReconciliationEngine:
    """
    MKYS ve TDMS hareketlerinin uzlaştırılmasını yönetir.
    """

    def __init__(self) -> None:
        self._opening_matcher = OpeningMatcher()
        self._entry_matcher = EntryMatcher()
        self._transfer_matcher = TransferMatcher()
        self._consumption_matcher = ConsumptionMatcher()

    def reconcile(
        self,
        mkys: list[Movement],
        tdms: list[Movement],
    ) -> ReconciliationResult:
        opening_result = self._opening_matcher.match(
            mkys,
            tdms,
        )

        entry_result = self._entry_matcher.match(
            mkys,
            tdms,
        )

        transfer_result = self._transfer_matcher.match(
            mkys,
            tdms,
        )

        consumption_differences = self._consumption_matcher.match(
            mkys,
            tdms,
        )

        return ReconciliationResult(
            matched=entry_result.matched,
            missing_in_tdms=entry_result.missing_in_tdms,
            missing_in_mkys=entry_result.missing_in_mkys,
            amount_differences=entry_result.amount_differences,
            consumption_differences=consumption_differences,
            opening_matched=opening_result.matched,
            opening_missing_in_tdms=opening_result.missing_in_tdms,
            opening_missing_in_mkys=opening_result.missing_in_mkys,
            transfer_matched=transfer_result.matched,
            transfer_missing_in_tdms=transfer_result.missing_in_tdms,
            transfer_missing_in_mkys=transfer_result.missing_in_mkys,
            transfer_amount_differences=transfer_result.amount_differences,
        )
