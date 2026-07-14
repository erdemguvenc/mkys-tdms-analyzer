from __future__ import annotations

from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.engine import ReconciliationEngine


def create_movement(
    *,
    source: str,
    tif_no: str,
    amount: str,
    description: str = "",
    movement_type: MovementType = MovementType.ENTRY,
) -> Movement:

    return Movement(
        source=source,
        movement_type=movement_type,
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

    tdms = []

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