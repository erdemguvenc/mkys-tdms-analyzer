from __future__ import annotations

from analyzer.models.movement import Movement
from analyzer.reconciliation.opening_matcher import OpeningMatcher
from tests.helpers.movement_factory import create_movement


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

    result = matcher.match(
        mkys,
        tdms,
    )

    assert len(result.matched) == 1
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0


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

    result = matcher.match(
        mkys,
        tdms,
    )

    assert len(result.matched) == 0
    assert len(result.missing_in_tdms) == 1
    assert len(result.missing_in_mkys) == 0


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

    result = matcher.match(
        mkys,
        tdms,
    )

    assert len(result.matched) == 0
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 1


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

    result = matcher.match(
        mkys,
        tdms,
    )

    assert len(result.matched) == 0
    assert len(result.missing_in_tdms) == 1
    assert len(result.missing_in_mkys) == 1


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

    result = matcher.match(
        mkys,
        tdms,
    )

    assert len(result.matched) == 0
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0


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

    result = matcher.match(
        mkys,
        tdms,
    )

    assert len(result.matched) == 2
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0
