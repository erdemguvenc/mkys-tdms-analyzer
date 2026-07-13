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

    result = ReconciliationEngine().reconcile(
        [movement("100", "250")],
        [movement("100", "250")],
    )

    assert len(result.matched) == 1
    assert len(result.amount_differences) == 0
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0


def test_amount_difference():

    result = ReconciliationEngine().reconcile(
        [movement("100", "250")],
        [movement("100", "300")],
    )

    assert len(result.matched) == 0
    assert len(result.amount_differences) == 1
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0

    diff = result.amount_differences[0]

    assert diff.mkys.amount == Decimal("250")
    assert diff.tdms.amount == Decimal("300")


def test_missing_in_tdms():

    result = ReconciliationEngine().reconcile(
        [movement("100", "250")],
        [],
    )

    assert len(result.missing_in_tdms) == 1
    assert len(result.missing_in_mkys) == 0
    assert len(result.matched) == 0


def test_missing_in_mkys():

    result = ReconciliationEngine().reconcile(
        [],
        [movement("100", "250")],
    )

    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 1
    assert len(result.matched) == 0


def test_duplicate_tif_matches_independently():

    mkys = [
        movement("100", "100"),
        movement("100", "200"),
    ]

    tdms = [
        movement("100", "100"),
        movement("100", "200"),
    ]

    result = ReconciliationEngine().reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 2
    assert len(result.amount_differences) == 0
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0


def test_duplicate_tif_with_one_difference():

    mkys = [
        movement("100", "100"),
        movement("100", "200"),
    ]

    tdms = [
        movement("100", "100"),
        movement("100", "250"),
    ]

    result = ReconciliationEngine().reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 1
    assert len(result.amount_differences) == 1
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0


def test_large_dataset():

    mkys = [
        movement(str(i), str(i))
        for i in range(1000)
    ]

    tdms = [
        movement(str(i), str(i))
        for i in range(1000)
    ]

    result = ReconciliationEngine().reconcile(
        mkys,
        tdms,
    )

    assert len(result.matched) == 1000
    assert len(result.amount_differences) == 0
    assert len(result.missing_in_tdms) == 0
    assert len(result.missing_in_mkys) == 0


def test_engine_returns_consumption_differences() -> None:

    engine = ReconciliationEngine()

    mkys = [
        Movement(
            source="MKYS",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 5),
            amount=Decimal("500"),
        )
    ]

    tdms = [
        Movement(
            source="TDMS",
            movement_type=MovementType.CONSUMPTION,
            movement_date=date(2026, 1, 31),
            amount=Decimal("450"),
        )
    ]

    result = engine.reconcile(
        mkys,
        tdms,
    )

    assert len(result.consumption_differences) == 1

    difference = result.consumption_differences[0]

    assert difference.year == 2026
    assert difference.month == 1

    assert difference.mkys_amount == Decimal("500")
    assert difference.tdms_amount == Decimal("450")

    assert difference.difference == Decimal("50")