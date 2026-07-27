from __future__ import annotations

from dataclasses import dataclass

from analyzer.reconciliation.result import ReconciliationResult


@dataclass(slots=True)
class DashboardSummary:

    total_records: int

    matched_records: int

    missing_in_mkys: int

    missing_in_tdms: int

    amount_difference_count: int

    consumption_difference_count: int

    @classmethod
    def from_result(
        cls,
        result: ReconciliationResult,
    ) -> "DashboardSummary":

        return cls(
            total_records=(
                len(result.matched)
                + len(result.missing_in_tdms)
            ),
            matched_records=len(result.matched),
            missing_in_mkys=len(result.missing_in_mkys),
            missing_in_tdms=len(result.missing_in_tdms),
            amount_difference_count=len(result.amount_differences),
            consumption_difference_count=len(
                result.consumption_differences
            ),
        )