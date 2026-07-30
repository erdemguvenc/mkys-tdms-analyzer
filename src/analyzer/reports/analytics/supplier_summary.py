from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from analyzer.reconciliation.result import ReconciliationResult


@dataclass(slots=True)
class SupplierSummary:
    """
    Dashboard için tedarikçi bazlı özet.
    """

    supplier: str

    total_records: int

    matched_records: int

    missing_in_mkys: int

    missing_in_tdms: int

    amount_difference_count: int

    total_amount: Decimal

    @property
    def match_rate(
        self,
    ) -> float:
        """
        Tedarikçi bazındaki eşleşme oranı (%).
        """

        if self.total_records == 0:

            return 0.0

        return (
            self.matched_records
            / self.total_records
            * 100
        )

    @classmethod
    def from_result(
        cls,
        result: ReconciliationResult,
    ) -> list["SupplierSummary"]:
        """
        Uzlaştırma sonucundan tedarikçi bazlı özetleri oluşturur.
        """

        grouped: dict[str, SupplierSummary] = {}

        #
        # Eşleşen kayıtlar
        #
        for movement in result.matched:

            summary = cls._get_or_create_summary(
                grouped,
                movement.supplier,
            )

            summary.total_records += 1
            summary.matched_records += 1
            summary.total_amount += movement.amount

        #
        # MKYS'de eksik kayıtlar
        #
        for movement in result.missing_in_mkys:

            summary = cls._get_or_create_summary(
                grouped,
                movement.supplier,
            )

            summary.total_records += 1
            summary.missing_in_mkys += 1
            summary.total_amount += movement.amount

        #
        # TDMS'de eksik kayıtlar
        #
        for movement in result.missing_in_tdms:

            summary = cls._get_or_create_summary(
                grouped,
                movement.supplier,
            )

            summary.total_records += 1
            summary.missing_in_tdms += 1
            summary.total_amount += movement.amount

        #
        # Tutar farklılıkları
        #
        for difference in result.amount_differences:

            summary = cls._get_or_create_summary(
                grouped,
                difference.mkys.supplier,
            )

            summary.amount_difference_count += 1

        return sorted(
            grouped.values(),
            key=lambda supplier: (
                supplier.total_records,
                supplier.total_amount,
            ),
            reverse=True,
        )

    @classmethod
    def _get_or_create_summary(
        cls,
        grouped: dict[str, "SupplierSummary"],
        supplier: str,
    ) -> "SupplierSummary":
        """
        İlgili tedarikçi özetini döndürür.
        Yoksa yeni oluşturur.
        """

        supplier = supplier or "Bilinmeyen"

        if supplier not in grouped:

            grouped[supplier] = cls(
                supplier=supplier,
                total_records=0,
                matched_records=0,
                missing_in_mkys=0,
                missing_in_tdms=0,
                amount_difference_count=0,
                total_amount=Decimal("0"),
            )

        return grouped[supplier]