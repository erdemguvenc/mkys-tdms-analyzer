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
