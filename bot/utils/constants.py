from enum import Enum
from dataclasses import dataclass


class FarmSizes(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


@dataclass
class PlotSize:
    rows: int
    columns: int


FARM_SIZE = {
    FarmSizes.SMALL: PlotSize(rows=3, columns=3),
    FarmSizes.MEDIUM: PlotSize(rows=5, columns=7),
    FarmSizes.LARGE: PlotSize(rows=7, columns=7),
}
