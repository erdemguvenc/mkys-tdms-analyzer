from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType


def movement(
    *,
    year: int = 2026,
    month: int = 1,
    day: int = 1,
    amount: Decimal = Decimal("100"),
    quantity: Decimal = Decimal("1"),
) -> Movement:
    return Movement(
        source="MKYS",
        movement_type=MovementType.ENTRY,
        movement_date=date(year, month, day),
        tif_no="TIF-1",
        voucher_no="VCH-1",
        document_no="DOC-1",
        invoice_no="INV-1",
        supplier="TEST",
        amount=amount,
        quantity=quantity,
        description="Test",
    )
