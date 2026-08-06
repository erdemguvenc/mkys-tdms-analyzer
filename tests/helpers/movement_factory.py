from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType


def create_movement(
    *,
    source: str = "MKYS",
    movement_type: MovementType = MovementType.ENTRY,
    tif_no: str = "TIF-1",
    voucher_no: str = "VCH-1",
    document_no: str = "DOC-1",
    invoice_no: str = "INV-1",
    supplier: str = "TEST",
    amount: Decimal | str = Decimal("100"),
    quantity: Decimal | str = Decimal("1"),
    description: str = "Test",
    year: int = 2026,
    month: int = 1,
    day: int = 1,
) -> Movement:
    return Movement(
        source=source,
        movement_type=movement_type,
        movement_date=date(year, month, day),
        tif_no=tif_no,
        voucher_no=voucher_no,
        document_no=document_no,
        invoice_no=invoice_no,
        supplier=supplier,
        amount=Decimal(str(amount)),
        quantity=Decimal(str(quantity)),
        description=description,
    )
