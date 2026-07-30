from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from analyzer.reconciliation.result import ReconciliationResult


@dataclass(slots=True)
class TopDifferenceSummary:
    """
    En büyük tutar farklarını temsil eder.
    """

    tif_no: str

    stock_code: str

    stock_name: str

    supplier: str

    mkys_amount: Decimal

    tdms_amount: Decimal

    difference: Decimal

    @classmethod
    def from_result(
        cls,
        result: ReconciliationResult,
        limit: int = 10,
    ) -> list["TopDifferenceSummary"]:

        summaries: list[TopDifferenceSummary] = []

        for item in result.amount_differences:

            summaries.append(
                cls(
                    tif_no=item.mkys.tif_no,
                    stock_code=item.mkys.stock_code,
                    stock_name=item.mkys.stock_name,
                    supplier=item.mkys.supplier,
                    mkys_amount=item.mkys.amount,
                    tdms_amount=item.tdms.amount,
                    difference=abs(
                        item.mkys.amount
                        - item.tdms.amount
                    ),
                )
            )

        summaries.sort(
            key=lambda x: x.difference,
            reverse=True,
        )

        return summaries[:limit]