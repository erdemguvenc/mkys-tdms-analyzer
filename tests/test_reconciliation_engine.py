from __future__ import annotations

from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.engine import ReconciliationEngine
from tests.helpers.movement_factory import create_movement


def test_reconcile_matching_entries() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="100",
            amount="1000",
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="100",
            amount="1000",
        )
    ]

    result = engine.reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 1
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0
    assert len(result.amount_differences) == 0


def test_reconcile_amount_difference() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="100",
            amount="100",
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="100",
            amount="200",
        )
    ]

    result = engine.reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 0
    assert len(result.amount_differences) == 1


def test_reconcile_missing_in_tdms() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="100",
            amount="100",
        )
    ]

    result = engine.reconcile(
        mkys,
        [],
    )

    assert len(result.missing_in_tdms) == 1
    assert len(result.missing_in_mkys) == 0


def test_reconcile_missing_in_mkys() -> None:
    engine = ReconciliationEngine()

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="100",
            amount="100",
        )
    ]

    result = engine.reconcile(
        [],
        tdms,
    )

    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 1


def test_reconcile_consumption_difference() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="",
            amount="500",
            movement_type=MovementType.CONSUMPTION,
        )
    ]

    tdms: list[Movement] = []

    result = engine.reconcile(
        mkys,
        tdms,
    )

    assert len(result.consumption_differences) == 1


def test_reconcile_opening_match() -> None:
    engine = ReconciliationEngine()

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

    result = engine.reconcile(
        mkys,
        tdms,
    )

    assert len(result.opening_matched) == 1
    assert len(result.opening_missing_in_tdms) == 0
    assert len(result.opening_missing_in_mkys) == 0


def test_reconcile_opening_missing_in_tdms() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="0",
            amount="1000",
        )
    ]

    result = engine.reconcile(
        mkys,
        [],
    )

    assert len(result.opening_matched) == 0
    assert len(result.opening_missing_in_tdms) == 1
    assert len(result.opening_missing_in_mkys) == 0


def test_reconcile_opening_missing_in_mkys() -> None:
    engine = ReconciliationEngine()

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="",
            amount="1000",
            description="MUHASEBE AÇILIŞ FİŞİ",
        )
    ]

    result = engine.reconcile(
        [],
        tdms,
    )

    assert len(result.opening_matched) == 0
    assert len(result.opening_missing_in_tdms) == 0
    assert len(result.opening_missing_in_mkys) == 1


def test_engine_matches_entries() -> None:
    engine = ReconciliationEngine()

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

    result = engine.reconcile(mkys, tdms)

    assert len(result.matched) == 1
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences


def test_engine_detects_amount_difference() -> None:
    engine = ReconciliationEngine()

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

    result = engine.reconcile(mkys, tdms)

    assert len(result.amount_differences) == 1
    assert not result.matched


def test_engine_detects_missing_in_tdms() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            tif_no="1001",
        )
    ]

    tdms: list[Movement] = []

    result = engine.reconcile(mkys, tdms)

    assert len(result.missing_in_tdms) == 1
    assert not result.missing_in_mkys


def test_engine_detects_missing_in_mkys() -> None:
    engine = ReconciliationEngine()

    mkys: list[Movement] = []

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="1001",
        )
    ]

    result = engine.reconcile(mkys, tdms)

    assert len(result.missing_in_mkys) == 1
    assert not result.missing_in_tdms


def test_engine_matches_multiple_entries() -> None:
    engine = ReconciliationEngine()

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

    result = engine.reconcile(mkys, tdms)

    assert len(result.matched) == 3
    assert not result.missing_in_tdms
    assert not result.missing_in_mkys
    assert not result.amount_differences


def test_engine_matches_transfer() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="T-100",
            amount=Decimal("100"),
            movement_type=MovementType.TRANSFER,
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="T-100",
            amount=Decimal("100"),
            movement_type=MovementType.TRANSFER,
        )
    ]

    result = engine.reconcile(
        mkys,
        tdms,
    )

    assert len(result.transfer_matched) == 1
    assert not result.transfer_missing_in_tdms
    assert not result.transfer_missing_in_mkys
    assert not result.transfer_amount_differences


def test_engine_detects_transfer_amount_difference() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="T-100",
            amount=Decimal("100"),
            movement_type=MovementType.TRANSFER,
        )
    ]

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="T-100",
            amount=Decimal("90"),
            movement_type=MovementType.TRANSFER,
        )
    ]

    result = engine.reconcile(
        mkys,
        tdms,
    )

    assert not result.transfer_matched
    assert len(result.transfer_amount_differences) == 1
    assert not result.transfer_missing_in_tdms
    assert not result.transfer_missing_in_mkys


def test_engine_detects_transfer_missing_in_tdms() -> None:
    engine = ReconciliationEngine()

    mkys = [
        create_movement(
            source="MKYS",
            tif_no="T-100",
            movement_type=MovementType.TRANSFER,
        )
    ]

    result = engine.reconcile(
        mkys,
        [],
    )

    assert not result.transfer_matched
    assert len(result.transfer_missing_in_tdms) == 1
    assert not result.transfer_missing_in_mkys
    assert not result.transfer_amount_differences


def test_engine_detects_transfer_missing_in_mkys() -> None:
    engine = ReconciliationEngine()

    tdms = [
        create_movement(
            source="TDMS",
            tif_no="T-100",
            movement_type=MovementType.TRANSFER,
        )
    ]

    result = engine.reconcile(
        [],
        tdms,
    )

    assert not result.transfer_matched
    assert not result.transfer_missing_in_tdms
    assert len(result.transfer_missing_in_mkys) == 1
    assert not result.transfer_amount_differences
