from __future__ import annotations

from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.entry_matcher import EntryMatcher
from tests.helpers.movement_factory import create_movement


def test_exact_match() -> None:
    matcher = EntryMatcher()

    mkys = [
        create_movement(
            tif_no="1001",
            amount=Decimal("100"),
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="1001",
            amount=Decimal("100"),
        )
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.matched) == 1
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0
    assert len(result.amount_differences) == 0


def test_amount_difference() -> None:
    matcher = EntryMatcher()

    mkys = [
        create_movement(
            tif_no="1001",
            amount=Decimal("100"),
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="1001",
            amount=Decimal("90"),
        )
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.amount_differences) == 1
    assert len(result.matched) == 0


def test_missing_in_tdms() -> None:
    matcher = EntryMatcher()

    mkys = [
        create_movement(
            tif_no="1001",
        )
    ]

    tdms: list[Movement] = []

    result = matcher.match(mkys, tdms)

    assert len(result.missing_in_tdms) == 1
    assert len(result.missing_in_mkys) == 0


def test_missing_in_mkys() -> None:
    matcher = EntryMatcher()

    mkys: list[Movement] = []

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="1001",
        )
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.missing_in_mkys) == 1
    assert len(result.missing_in_tdms) == 0


def test_multiple_matches() -> None:
    matcher = EntryMatcher()

    mkys = [
        create_movement(tif_no="1001"),
        create_movement(tif_no="1002"),
        create_movement(tif_no="1003"),
    ]

    tdms = [
        create_movement(source="TDMS", tif_no="1001"),
        create_movement(source="TDMS", tif_no="1002"),
        create_movement(source="TDMS", tif_no="1003"),
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.matched) == 3
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences


def test_ignores_non_entry_movements() -> None:
    matcher = EntryMatcher()

    mkys = [
        create_movement(
            movement_type=MovementType.CONSUMPTION,
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            movement_type=MovementType.CONSUMPTION,
        )
    ]

    result = matcher.match(mkys, tdms)

    assert not result.matched
