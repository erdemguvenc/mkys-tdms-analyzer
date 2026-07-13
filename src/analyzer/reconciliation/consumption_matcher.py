from __future__ import annotations

from decimal import Decimal

from .difference import ConsumptionDifference
from .grouping import MonthlyConsumptionGrouping


class ConsumptionMatcher:
    """
    MKYS tüketim toplamlarını
    TDMS tüketim toplamları ile karşılaştırır.
    """

    def match(
        self,
        mkys,
        tdms,
    ) -> list[ConsumptionDifference]:

        mkys_groups = MonthlyConsumptionGrouping.group(
            mkys
        )

        tdms_groups = MonthlyConsumptionGrouping.group(
            tdms
        )

        differences: list[ConsumptionDifference] = []

        months = (
            set(mkys_groups)
            | set(tdms_groups)
        )

        for key in sorted(months):

            mkys_total = mkys_groups.get(
                key,
                Decimal("0"),
            )

            tdms_total = tdms_groups.get(
                key,
                Decimal("0"),
            )

            if mkys_total != tdms_total:

                differences.append(
                    ConsumptionDifference(
                        year=key[0],
                        month=key[1],
                        mkys_amount=mkys_total,
                        tdms_amount=tdms_total,
                    )
                )

        return differences