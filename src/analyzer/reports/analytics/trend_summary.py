from __future__ import annotations

from dataclasses import dataclass

from analyzer.reconciliation.result import ReconciliationResult

from .monthly_summary import MonthlySummary


@dataclass(slots=True)
class TrendSummary:
    """
    Dashboard trend analizinde kullanılacak aylık özetler.
    """

    months: list[MonthlySummary]

    @classmethod
    def from_result(
        cls,
        result: ReconciliationResult,
    ) -> "TrendSummary":
        """
        Uzlaştırma sonucundan aylık trend özetini oluşturur.
        """

        grouped: dict[str, MonthlySummary] = {}

        #
        # Eşleşen kayıtlar
        #
        for movement in result.matched:

            month = movement.movement_date.strftime("%Y-%m")

            summary = cls._get_or_create_summary(
                grouped,
                month,
            )

            summary.total_records += 1
            summary.matched_records += 1

        #
        # TDMS'de eksik
        #
        for movement in result.missing_in_tdms:

            month = movement.movement_date.strftime("%Y-%m")

            summary = cls._get_or_create_summary(
                grouped,
                month,
            )

            summary.total_records += 1
            summary.missing_in_tdms += 1

        #
        # MKYS'de eksik
        #
        for movement in result.missing_in_mkys:

            month = movement.movement_date.strftime("%Y-%m")

            summary = cls._get_or_create_summary(
                grouped,
                month,
            )

            summary.total_records += 1
            summary.missing_in_mkys += 1

        #
        # Tutar farkları
        #
        for difference in result.amount_differences:

            month = difference.mkys.movement_date.strftime(
                "%Y-%m"
            )

            summary = cls._get_or_create_summary(
                grouped,
                month,
            )

            summary.amount_difference_count += 1

        #
        # Tüketim farkları
        #
        for difference in result.consumption_differences:

            month = (
                f"{difference.year:04d}-"
                f"{difference.month:02d}"
            )

            summary = cls._get_or_create_summary(
                grouped,
                month,
            )

            summary.consumption_difference_count += 1

        return cls(
            months=[
                grouped[key]
                for key in sorted(grouped)
            ],
        )

    @classmethod
    def _get_or_create_summary(
        cls,
        grouped: dict[str, MonthlySummary],
        month: str,
    ) -> MonthlySummary:
        """
        İlgili aya ait özeti döndürür.
        Yoksa yeni oluşturur.
        """

        if month not in grouped:

            grouped[month] = MonthlySummary(
                month=month,
                total_records=0,
                matched_records=0,
                missing_in_mkys=0,
                missing_in_tdms=0,
                amount_difference_count=0,
                consumption_difference_count=0,
            )

        return grouped[month]