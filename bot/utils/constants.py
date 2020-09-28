from enum import Enum
from dataclasses import dataclass
import ujson

import discord


class FarmSizes(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class InventorySizes(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


@dataclass
class PlotDimensions:
    rows: int
    columns: int


@dataclass
class PlotCoordinate:
    row: int
    column: int


class PlotActions(Enum):
    HARVEST = 1
    WATER = 2
    PLANT = 3


FARM_DIMENSIONS = {
    FarmSizes.SMALL: PlotDimensions(rows=3, columns=3),
    FarmSizes.MEDIUM: PlotDimensions(rows=5, columns=7),
    FarmSizes.LARGE: PlotDimensions(rows=7, columns=7),
}

PLAYER_BALANCE = 1000

with open("crop_types.json") as f:
    CROP_DATA = ujson.load(f)

COLOR_ERROR = discord.Color.red()

COLOR_SUCCESS = discord.Color.green()
