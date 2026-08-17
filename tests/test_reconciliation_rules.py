from analyzer.models.movement_type import MovementType
from analyzer.reconciliation.rules import (
    RECONCILIATION_RULES,
    Cardinality,
    ReconciliationKey,
    ReconciliationRule,
)

EXPECTED_RULES = {
    MovementType.ENTRY: (
        ReconciliationKey.TIF,
        Cardinality.ONE_TO_ONE,
    ),
    MovementType.CONSUMPTION: (
        ReconciliationKey.MONTH,
        Cardinality.MANY_TO_ONE,
    ),
    MovementType.TRANSFER: (
        ReconciliationKey.TIF,
        Cardinality.ONE_TO_ONE,
    ),
    MovementType.SCRAP: (
        ReconciliationKey.TIF,
        Cardinality.ONE_TO_ONE,
    ),
    MovementType.DONATION: (
        ReconciliationKey.TIF,
        Cardinality.ONE_TO_ONE,
    ),
    MovementType.COUNT_SURPLUS: (
        ReconciliationKey.TIF,
        Cardinality.ONE_TO_ONE,
    ),
    MovementType.COUNT_DEFICIT: (
        ReconciliationKey.TIF,
        Cardinality.ONE_TO_ONE,
    ),
}


def test_reconciliation_rules():
    for movement_type, (expected_key, expected_cardinality) in EXPECTED_RULES.items():
        rule = RECONCILIATION_RULES[movement_type]

        assert isinstance(rule, ReconciliationRule)
        assert rule.key is expected_key
        assert rule.cardinality is expected_cardinality


def test_donation_uses_tif_one_to_one_rule():
    rule = RECONCILIATION_RULES[MovementType.DONATION]

    assert rule.key is ReconciliationKey.TIF
    assert rule.cardinality is Cardinality.ONE_TO_ONE


def test_count_surplus_uses_tif_one_to_one_rule():
    rule = RECONCILIATION_RULES[MovementType.COUNT_SURPLUS]

    assert rule.key is ReconciliationKey.TIF
    assert rule.cardinality is Cardinality.ONE_TO_ONE


def test_count_deficit_uses_tif_one_to_one_rule():
    rule = RECONCILIATION_RULES[MovementType.COUNT_DEFICIT]

    assert rule.key is ReconciliationKey.TIF
    assert rule.cardinality is Cardinality.ONE_TO_ONE


def test_other_has_no_reconciliation_rule():
    assert MovementType.OTHER not in RECONCILIATION_RULES
