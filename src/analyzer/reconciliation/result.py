from __future__ import annotations

from dataclasses import dataclass, field

from analyzer.models.movement import Movement

from .consumption import ConsumptionMatch
from .difference import AmountDifference, ConsumptionDifference
from .duplicate import DuplicateMovement


@dataclass(slots=True)
class ReconciliationResult:
    """
    Uzlaştırma sonucu.

    Alanlar:

    - matched:
        Giriş hareketlerinde eşleşen kayıtlar.

    - missing_in_tdms:
        MKYS'de olup TDMS'de bulunamayan giriş kayıtları.

    - missing_in_mkys:
        TDMS'de olup MKYS'de bulunamayan giriş kayıtları.

    - amount_differences:
        Giriş hareketlerindeki tutar farklılıkları.

    - consumption_matched:
        Aylık tüketim uzlaştırmasında eşleşen aylar.

    - consumption_differences:
        Aylık tüketim uzlaştırmasında oluşan farklar.

    - duplicate_movements:
        ONE_TO_ONE reconciliation kapsamında aynı TİF numarasıyla
        birden fazla bulunan hareketler.

    - opening_matched:
        Eşleşen açılış kayıtları.

    - opening_missing_in_tdms:
        MKYS açılış kayıtlarından TDMS'de bulunamayanlar.

    - opening_missing_in_mkys:
        TDMS açılış kayıtlarından MKYS'de bulunamayanlar.

    - scrap_matched:
        Eşleşen hurda kayıtları.

    - scrap_missing_in_tdms:
        MKYS'de olup TDMS'de bulunamayan hurda kayıtları.

    - scrap_missing_in_mkys:
        TDMS'de olup MKYS'de bulunamayan hurda kayıtları.

    - scrap_amount_differences:
        Aynı hurda hareketindeki tutar farklılıkları.

    - transfer_matched:
        Eşleşen transfer kayıtları.

    - transfer_missing_in_tdms:
        MKYS'de olup TDMS'de bulunamayan transfer kayıtları.

    - transfer_missing_in_mkys:
        TDMS'de olup MKYS'de bulunamayan transfer kayıtları.

    - transfer_amount_differences:
        Aynı transfer hareketindeki tutar farklılıkları.
    """

    matched: list[Movement] = field(
        default_factory=list,
    )

    missing_in_tdms: list[Movement] = field(
        default_factory=list,
    )

    missing_in_mkys: list[Movement] = field(
        default_factory=list,
    )

    amount_differences: list[AmountDifference] = field(
        default_factory=list,
    )

    consumption_matched: list[ConsumptionMatch] = field(
        default_factory=list,
    )

    consumption_differences: list[ConsumptionDifference] = field(
        default_factory=list,
    )

    duplicate_movements: list[DuplicateMovement] = field(
        default_factory=list,
    )

    opening_matched: list[Movement] = field(
        default_factory=list,
    )

    opening_missing_in_tdms: list[Movement] = field(
        default_factory=list,
    )

    opening_missing_in_mkys: list[Movement] = field(
        default_factory=list,
    )

    scrap_matched: list[Movement] = field(
        default_factory=list,
    )

    scrap_missing_in_tdms: list[Movement] = field(
        default_factory=list,
    )

    scrap_missing_in_mkys: list[Movement] = field(
        default_factory=list,
    )

    scrap_amount_differences: list[AmountDifference] = field(
        default_factory=list,
    )

    transfer_matched: list[Movement] = field(
        default_factory=list,
    )

    transfer_missing_in_tdms: list[Movement] = field(
        default_factory=list,
    )

    transfer_missing_in_mkys: list[Movement] = field(
        default_factory=list,
    )

    transfer_amount_differences: list[AmountDifference] = field(
        default_factory=list,
    )
