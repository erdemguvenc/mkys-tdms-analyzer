from __future__ import annotations

from datetime import date
from decimal import Decimal

from analyzer.models.movement import Movement
from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.consumption_matcher import (
    ConsumptionMatcher,
)


def movement(
    movement_date: date,
    amount: str,
) -> Movement:
    return Movement(
        source="MKYS",
        movement_type=MovementType.CONSUMPTION,
        movement_date=movement_date,
        amount=Decimal(amount),
    )


def test_same_month_same_total() -> None:

    mkys = [
        movement(date(2026, 1, 5), "100"),
        movement(date(2026, 1, 10), "200"),
        movement(date(2026, 1, 20), "300"),
    ]

    tdms = [
        movement(date(2026, 1, 31), "600"),
    ]

    matcher = ConsumptionMatcher()

    differences = matcher.match(
        mkys,
        tdms,
    )

    assert differences == []


def test_same_month_different_total() -> None:

    mkys = [
        movement(date(2026, 1, 5), "100"),
        movement(date(2026, 1, 10), "200"),
        movement(date(2026, 1, 20), "300"),
    ]

    tdms = [
        movement(date(2026, 1, 31), "550"),
    ]

    matcher = ConsumptionMatcher()

    differences = matcher.match(
        mkys,
        tdms,
    )

    assert len(differences) == 1

    diff = differences[0]

    assert diff.year == 2026
    assert diff.month == 1
    assert diff.mkys_amount == Decimal("600")
    assert diff.tdms_amount == Decimal("550")
    assert diff.difference == Decimal("50")


def test_two_months() -> None:

    mkys = [
        movement(date(2026, 1, 5), "100"),
        movement(date(2026, 2, 5), "300"),
    ]

    tdms = [
        movement(date(2026, 1, 31), "100"),
        movement(date(2026, 2, 28), "250"),
    ]

    matcher = ConsumptionMatcher()

    differences = matcher.match(
        mkys,
        tdms,
    )

    assert len(differences) == 1

    diff = differences[0]

    assert diff.year == 2026
    assert diff.month == 2
    assert diff.difference == Decimal("50")


def test_month_exists_only_in_mkys() -> None:

    mkys = [
        movement(date(2026, 3, 5), "400"),
    ]

    tdms = []

    matcher = ConsumptionMatcher()

    differences = matcher.match(
        mkys,
        tdms,
    )

    assert len(differences) == 1

    diff = differences[0]

    assert diff.year == 2026
    assert diff.month == 3
    assert diff.mkys_amount == Decimal("400")
    assert diff.tdms_amount == Decimal("0")
    assert diff.difference == Decimal("400")


def test_month_exists_only_in_tdms() -> None:

    mkys = []

    tdms = [
        movement(date(2026, 4, 30), "900"),
    ]

    matcher = ConsumptionMatcher()

    differences = matcher.match(
        mkys,
        tdms,
    )

    assert len(differences) == 1

    diff = differences[0]

    assert diff.year == 2026
    assert diff.month == 4
    assert diff.mkys_amount == Decimal("0")
    assert diff.tdms_amount == Decimal("900")
    assert diff.difference == Decimal("-900")


def test_multiple_movements_grouped_correctly() -> None:

    mkys = [
        movement(date(2026, 5, 1), "100"),
        movement(date(2026, 5, 2), "150"),
        movement(date(2026, 5, 3), "250"),
        movement(date(2026, 5, 4), "500"),
    ]

    tdms = [
        movement(date(2026, 5, 31), "1000"),
    ]

    matcher = ConsumptionMatcher()

    differences = matcher.match(
        mkys,
        tdms,
    )

    assert differences == []