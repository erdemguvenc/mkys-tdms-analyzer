from decimal import Decimal

from analyzer.reconciliation.difference import (
    AmountDifference,
    ConsumptionDifference,
)
from analyzer.reconciliation.result import ReconciliationResult

from .movement_factory import movement


def reconciliation_result() -> ReconciliationResult:
    return ReconciliationResult(
        matched=[
            movement(year=2025, month=1),
            movement(year=2025, month=1),
        ],
        missing_in_tdms=[
            movement(year=2025, month=2),
        ],
        missing_in_mkys=[
            movement(year=2025, month=3),
        ],
        amount_differences=[
            AmountDifference(
                mkys=movement(year=2025, month=1),
                tdms=movement(year=2025, month=1),
            ),
        ],
        consumption_differences=[
            ConsumptionDifference(
                year=2025,
                month=1,
                mkys_amount=Decimal("100"),
                tdms_amount=Decimal("95"),
            ),
            ConsumptionDifference(
                year=2025,
                month=2,
                mkys_amount=Decimal("200"),
                tdms_amount=Decimal("180"),
            ),
        ],
    )