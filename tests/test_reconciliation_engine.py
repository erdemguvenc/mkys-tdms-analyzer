from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.engine import ReconciliationEngine


def movement(
    tif: str,
    amount: str,
) -> Movement:

    return Movement(
        source="TEST",
        movement_type=MovementType.ENTRY,
        movement_date=date(2026, 1, 1),
        tif_no=tif,
        amount=Decimal(amount),
    )


def test_matching_entry():

    mkys = [
        movement("100", "250"),
    ]

    tdms = [
        movement("100", "250"),
    ]

    result = ReconciliationEngine().reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 1

    assert len(result.missing_in_tdms) == 0

    assert len(result.missing_in_mkys) == 0


def test_missing_tdms():

    mkys = [
        movement("100", "250"),
    ]

    tdms = []

    result = ReconciliationEngine().reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 0

    assert len(result.missing_in_tdms) == 1

    assert len(result.missing_in_mkys) == 0


def test_missing_mkys():

    mkys = []

    tdms = [
        movement("100", "250"),
    ]

    result = ReconciliationEngine().reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 0

    assert len(result.missing_in_tdms) == 0

    assert len(result.missing_in_mkys) == 1


def test_amount_difference():

    mkys = [
        movement("100", "250"),
    ]

    tdms = [
        movement("100", "300"),
    ]

    result = ReconciliationEngine().reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 0

    assert len(result.missing_in_tdms) == 1

    assert len(result.missing_in_mkys) == 1