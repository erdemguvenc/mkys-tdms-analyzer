from __future__ import annotations

from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.scrap_matcher import ScrapMatcher
from tests.helpers.movement_factory import create_movement


def test_scrap_match_is_found() -> None:
    matcher = ScrapMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        )
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.matched) == 1
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences


def test_scrap_amount_difference_is_detected() -> None:
    matcher = ScrapMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="S-100",
            amount=Decimal("90"),
            movement_type=MovementType.SCRAP,
        )
    ]

    result = matcher.match(mkys, tdms)

    assert not result.matched
    assert len(result.amount_differences) == 1
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys


def test_scrap_missing_in_tdms() -> None:
    matcher = ScrapMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        )
    ]

    tdms: list[Movement] = []

    result = matcher.match(mkys, tdms)

    assert not result.matched
    assert len(result.missing_in_tdms) == 1
    assert not result.missing_in_mkys
    assert not result.amount_differences


def test_scrap_missing_in_mkys() -> None:
    matcher = ScrapMatcher()

    mkys: list[Movement] = []

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        )
    ]

    result = matcher.match(mkys, tdms)

    assert not result.matched
    assert not result.missing_in_tdms
    assert len(result.missing_in_mkys) == 1
    assert not result.amount_differences


def test_non_scrap_records_are_ignored() -> None:
    matcher = ScrapMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.ENTRY,
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.ENTRY,
        )
    ]

    result = matcher.match(mkys, tdms)

    assert not result.matched
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences


def test_scrap_missing_tif_is_missing_in_tdms() -> None:
    matcher = ScrapMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="S-200",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        )
    ]

    result = matcher.match(mkys, tdms)

    assert not result.matched
    assert len(result.missing_in_tdms) == 1
    assert len(result.missing_in_mkys) == 1
    assert not result.amount_differences


def test_multiple_scrap_records_are_matched() -> None:
    matcher = ScrapMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        ),
        create_movement(
            source="MKYS",
            tif_no="S-200",
            amount=Decimal("200"),
            movement_type=MovementType.SCRAP,
        ),
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="S-100",
            amount=Decimal("100"),
            movement_type=MovementType.SCRAP,
        ),
        create_movement(
            source="TDMS",
            tif_no="S-200",
            amount=Decimal("200"),
            movement_type=MovementType.SCRAP,
        ),
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.matched) == 2
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences
