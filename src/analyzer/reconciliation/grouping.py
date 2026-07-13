from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType


class MonthlyConsumptionGrouping:
    """
    Consumption hareketlerini ay bazında toplar.

    Key:
        (year, month)

    Value:
        Decimal toplam tutar
    """

    @staticmethod
    def group(
        movements: list[Movement],
    ) -> dict[tuple[int, int], Decimal]:

        totals: dict[tuple[int, int], Decimal] = defaultdict(
            lambda: Decimal("0")
        )

        for movement in movements:

            if movement.movement_type != MovementType.CONSUMPTION:
                continue

            key = (
                movement.movement_date.year,
                movement.movement_date.month,
            )

            totals[key] += movement.amount

        return dict(totals)