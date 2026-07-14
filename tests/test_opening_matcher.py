from __future__ import annotations

from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.opening_matcher import OpeningMatcher


def create_movement(
    *,
    source: str,
    tif_no: str,
    amount: str,
    description: str = "",
) -> Movement:

    return Movement(
        source=source,
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 1),
        tif_no=tif_no,
        voucher_no="",
        document_no="",
        invoice_no="",
        amount=Decimal(amount),
        description=description,
        warehouse="",
        budget_type="",
        stock_code="",
        stock_name="",
        supplier="",
        quantity=Decimal("0"),
    )


def test_opening_match_is_found() -> None:

    matcher = OpeningMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="0",
            amount="1000",
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="",
            amount="1000",
            description="MUHASEBE AÇILIŞ FİŞİ",
        )
    ]

    matched, missing_tdms, missing_mkys = matcher.match(
        mkys,
        tdms,
    )

    assert len(matched) == 1
    assert len(missing_tdms) == 0
    assert len(missing_mkys) == 0


def test_missing_in_tdms() -> None:

    matcher = OpeningMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="0",
            amount="500",
        )
    ]

    tdms: list[Movement] = []

    matched, missing_tdms, missing_mkys = matcher.match(
        mkys,
        tdms,
    )

    assert len(matched) == 0
    assert len(missing_tdms) == 1
    assert len(missing_mkys) == 0


def test_missing_in_mkys() -> None:

    matcher = OpeningMatcher()

    mkys: list[Movement] = []

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="",
            amount="500",
            description="MUHASEBE AÇILIŞ FİŞİ",
        )
    ]

    matched, missing_tdms, missing_mkys = matcher.match(
        mkys,
        tdms,
    )

    assert len(matched) == 0
    assert len(missing_tdms) == 0
    assert len(missing_mkys) == 1


def test_amount_difference_is_not_matched() -> None:

    matcher = OpeningMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="0",
            amount="100",
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="",
            amount="200",
            description="MUHASEBE AÇILIŞ FİŞİ",
        )
    ]

    matched, missing_tdms, missing_mkys = matcher.match(
        mkys,
        tdms,
    )

    assert len(matched) == 0
    assert len(missing_tdms) == 1
    assert len(missing_mkys) == 1


def test_non_opening_records_are_ignored() -> None:

    matcher = OpeningMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="12345",
            amount="100",
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="12345",
            amount="100",
            description="GİRİŞ FİŞİ",
        )
    ]

    matched, missing_tdms, missing_mkys = matcher.match(
        mkys,
        tdms,
    )

    assert matched == []
    assert missing_tdms == []
    assert missing_mkys == []


def test_multiple_openings_are_matched() -> None:

    matcher = OpeningMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="0",
            amount="100",
        ),
        create_movement(
            source="MKYS",
            tif_no="0",
            amount="200",
        ),
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="",
            amount="100",
            description="MUHASEBE AÇILIŞ FİŞİ",
        ),
        create_movement(
            source="TDMS",
            tif_no="",
            amount="200",
            description="MUHASEBE AÇILIŞ FİŞİ",
        ),
    ]

    matched, missing_tdms, missing_mkys = matcher.match(
        mkys,
        tdms,
    )

    assert len(matched) == 2
    assert len(missing_tdms) == 0
    assert len(missing_mkys) == 0