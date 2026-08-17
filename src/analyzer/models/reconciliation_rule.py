from dataclasses import dataclass
from enum import Enum


class GroupingStrategy(Enum):
    TIF = "tif"
    MONTH = "month"


class MatchingStrategy(Enum):
    ONE_TO_ONE = "one_to_one"
    MANY_TO_ONE = "many_to_one"


@dataclass(frozen=True)
class ReconciliationRule:
    grouping_strategy: GroupingStrategy
    matching_strategy: MatchingStrategy
