from __future__ import annotations

from dataclasses import dataclass

from analyzer.models.movement import Movement


@dataclass(frozen=True, slots=True)
class DuplicateMovement:
    """
    Aynı TİF numarasıyla birden fazla bulunan hareketleri temsil eder.

    Duplicate kontrolü yalnızca TIF tabanlı ONE_TO_ONE
    reconciliation kurallarında kullanılmalıdır.

    Attributes
    ----------
    tif_no:
        Duplicate olan TİF numarası.

    movements:
        Aynı TİF numarasına sahip hareketler.
    """

    tif_no: str
    movements: list[Movement]
