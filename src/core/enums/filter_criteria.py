from enum import Enum


class FilterCriteriaEnum(Enum):
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    LT = "lt"
    GTE = "gte"
    LTE = "lte"
    BETWEEN = "between"
    LIKE = "like"
    CONTAINS = "contains"
