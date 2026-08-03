from __future__ import annotations

from dataclasses import dataclass

from analyzer.reconciliation.result import ReconciliationResult


@dataclass(slots=True)
class WarehouseSummary:
    """
    Ambar bazlı uzlaştırma özeti.
    """

    warehouse: str

    total_records: int

    matched_records: int

    missing_in_mkys: int

    missing_in_tdms: int

    amount_difference_count: int

    @property
    def match_rate(self) -> float:
        if self.total_records == 0:
            return 0.0

        return self.matched_records / self.total_records * 100

    @classmethod
    def from_result(
        cls,
        result: ReconciliationResult,
    ) -> list["WarehouseSummary"]:
        grouped: dict[str, WarehouseSummary] = {}

        #
        # Eşleşen kayıtlar
        #
        for movement in result.matched:
            summary = grouped.setdefault(
                movement.warehouse,
                cls(
                    warehouse=movement.warehouse,
                    total_records=0,
                    matched_records=0,
                    missing_in_mkys=0,
                    missing_in_tdms=0,
                    amount_difference_count=0,
                ),
            )

            summary.total_records += 1
            summary.matched_records += 1

        #
        # TDMS'de eksik
        #
        for movement in result.missing_in_tdms:
            summary = grouped.setdefault(
                movement.warehouse,
                cls(
                    warehouse=movement.warehouse,
                    total_records=0,
                    matched_records=0,
                    missing_in_mkys=0,
                    missing_in_tdms=0,
                    amount_difference_count=0,
                ),
            )

            summary.total_records += 1
            summary.missing_in_tdms += 1

        #
        # MKYS'de eksik
        #
        for movement in result.missing_in_mkys:
            summary = grouped.setdefault(
                movement.warehouse,
                cls(
                    warehouse=movement.warehouse,
                    total_records=0,
                    matched_records=0,
                    missing_in_mkys=0,
                    missing_in_tdms=0,
                    amount_difference_count=0,
                ),
            )

            summary.total_records += 1
            summary.missing_in_mkys += 1

        #
        # Tutar farkları
        #
        for difference in result.amount_differences:
            warehouse = difference.mkys.warehouse

            summary = grouped.setdefault(
                warehouse,
                cls(
                    warehouse=warehouse,
                    total_records=0,
                    matched_records=0,
                    missing_in_mkys=0,
                    missing_in_tdms=0,
                    amount_difference_count=0,
                ),
            )

            summary.amount_difference_count += 1

        return sorted(
            grouped.values(),
            key=lambda x: x.total_records,
            reverse=True,
        )
