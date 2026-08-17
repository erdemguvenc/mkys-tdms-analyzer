from dataclasses import dataclass
from enum import Enum

from analyzer.models.movement_type import MovementType


class ReconciliationKey(Enum):
    TIF = "tif"
    MONTH = "month"


class Cardinality(Enum):
    ONE_TO_ONE = "one_to_one"
    MANY_TO_ONE = "many_to_one"


@dataclass(frozen=True, slots=True)
class ReconciliationRule:
    key: ReconciliationKey
    cardinality: Cardinality


RECONCILIATION_RULES = {
    MovementType.ENTRY: ReconciliationRule(
        key=ReconciliationKey.TIF,
        cardinality=Cardinality.ONE_TO_ONE,
    ),
    MovementType.CONSUMPTION: ReconciliationRule(
        key=ReconciliationKey.MONTH,
        cardinality=Cardinality.MANY_TO_ONE,
    ),
    MovementType.TRANSFER: ReconciliationRule(
        key=ReconciliationKey.TIF,
        cardinality=Cardinality.ONE_TO_ONE,
    ),
    MovementType.SCRAP: ReconciliationRule(
        key=ReconciliationKey.TIF,
        cardinality=Cardinality.ONE_TO_ONE,
    ),
    MovementType.DONATION: ReconciliationRule(
        key=ReconciliationKey.TIF,
        cardinality=Cardinality.ONE_TO_ONE,
    ),
    MovementType.COUNT_SURPLUS: ReconciliationRule(
        key=ReconciliationKey.TIF,
        cardinality=Cardinality.ONE_TO_ONE,
    ),
    MovementType.COUNT_DEFICIT: ReconciliationRule(
        key=ReconciliationKey.TIF,
        cardinality=Cardinality.ONE_TO_ONE,
    ),
}
