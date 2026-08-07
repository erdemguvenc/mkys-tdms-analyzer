from __future__ import annotations

from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.transfer_matcher import TransferMatcher
from tests.helpers.movement_factory import create_movement


def test_exact_match() -> None:
    matcher = TransferMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            movement_type=MovementType.TRANSFER,
            tif_no="1001",
            amount=Decimal("100"),
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            movement_type=MovementType.TRANSFER,
            tif_no="1001",
            amount=Decimal("100"),
        )
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.matched) == 1
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences


def test_amount_difference() -> None:
    matcher = TransferMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            movement_type=MovementType.TRANSFER,
            tif_no="1001",
            amount=Decimal("100"),
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            movement_type=MovementType.TRANSFER,
            tif_no="1001",
            amount=Decimal("90"),
        )
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.amount_differences) == 1
    assert not result.matched


def test_missing_in_tdms() -> None:
    matcher = TransferMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            movement_type=MovementType.TRANSFER,
            tif_no="1001",
        )
    ]

    tdms: list[Movement] = []

    result = matcher.match(mkys, tdms)

    assert len(result.missing_in_tdms) == 1
    assert not result.missing_in_mkys


def test_missing_in_mkys() -> None:
    matcher = TransferMatcher()

    mkys: list[Movement] = []

    tdms = [
        create_movement(
            source="TDMS",
            movement_type=MovementType.TRANSFER,
            tif_no="1001",
        )
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.missing_in_mkys) == 1
    assert not result.missing_in_tdms


def test_multiple_matches() -> None:
    matcher = TransferMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            movement_type=MovementType.TRANSFER,
            tif_no="1001",
        ),
        create_movement(
            source="MKYS",
            movement_type=MovementType.TRANSFER,
            tif_no="1002",
        ),
        create_movement(
            source="MKYS",
            movement_type=MovementType.TRANSFER,
            tif_no="1003",
        ),
    ]

    tdms = [
        create_movement(
            source="TDMS",
            movement_type=MovementType.TRANSFER,
            tif_no="1001",
        ),
        create_movement(
            source="TDMS",
            movement_type=MovementType.TRANSFER,
            tif_no="1002",
        ),
        create_movement(
            source="TDMS",
            movement_type=MovementType.TRANSFER,
            tif_no="1003",
        ),
    ]

    result = matcher.match(mkys, tdms)

    assert len(result.matched) == 3
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences


def test_ignores_non_transfer_movements() -> None:
    matcher = TransferMatcher()

    mkys = [
        create_movement(
            source="MKYS",
            movement_type=MovementType.ENTRY,
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            movement_type=MovementType.ENTRY,
        )
    ]

    result = matcher.match(mkys, tdms)

    assert not result.matched
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences
