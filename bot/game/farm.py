from bot.database.models import Farm as FarmModel
from bot.database.models import PlantedCrop
from bot.game.crop import Crop
from bot.utils.constants import (
    FarmSizes,
    FARM_DIMENSIONS,
    PlotCoordinate,
    PlotActions,
    CROP_DATA,
)
from discord import Embed
from typing import List, Optional


class Farm:
    def __init__(self, farm_id: int, size: FarmSizes, name: str):
        self.id = farm_id
        self.name = name
        self.size = size
        self.dimensions = FARM_DIMENSIONS.get(self.size)
        self.plot: List[List] = self.initialize_plot()

    @classmethod
    async def load(cls, player_id: int) -> "Farm":
        farm_model = await FarmModel.query.where(
            FarmModel.player_id == player_id
        ).gino.first()
        if farm_model is None:
            farm_model = await FarmModel.create(player_id=player_id)
        farm = Farm(
            farm_id=farm_model.id, size=FarmSizes(farm_model.size), name=farm_model.name
        )
        await farm.load_crops()
        return farm

    def initialize_plot(self) -> List[List[Optional[Crop]]]:
        return [
            [None for _ in range(self.dimensions.rows)]
            for _ in range(self.dimensions.columns)
        ]

    async def load_crops(self):
        crops = await PlantedCrop.query.where(PlantedCrop.farm_id == self.id).gino.all()
        for crop in crops:
            self.place_crop(
                Crop(
                    id=crop.id,
                    farm_id=crop.farm_id,
                    crop_id=crop.crop_id,
                    planted_at=crop.planted_at,
                ),
                row=crop.coord_row,
                column=crop.coord_column,
            )

    def validate_coordinate(self, row: int = None, column: int = None):
        if row is not None:
            if row >= self.dimensions.rows or row < 0:
                return False
        if column is not None:
            if column >= self.dimensions.columns or column < 0:
                return False
        return True

    def place_crop(self, crop: Crop, row: int, column: int):
        if not self.validate_coordinate(row=row, column=column):
            raise ValueError("Crop placement out of bounds")
        self.plot[row][column] = crop

    async def work_plot(self, action: PlotActions, row: int, column: int, crop_id: int):
        if not self.validate_coordinate(row, column):
            return
        if self.plot[row][column] is not None:

            await self.plot[row][column].work(action)
        else:
            if action is PlotActions.PLANT:
                self.plot[row][column] = await Crop.new(
                    farm_id=self.id, crop_id=crop_id, row=row, column=column
                )

    async def work_plots(
        self,
        action: PlotActions,
        coordinates: List[PlotCoordinate],
        crop_id: int = None,
    ):
        if not coordinates:
            for row in range(self.dimensions.rows):
                for column in range(self.dimensions.columns):
                    await self.work_plot(
                        action=action, row=row, column=column, crop_id=crop_id
                    )
        
        for coordinate in coordinates:
            await self.work_plot(
                action=action,
                row=coordinate.row,
                column=coordinate.column,
                crop_id=crop_id,
            )

    def display(self):
        farm_land = ""
        for row in self.plot:
            for crop in row:
                if crop is None:
                    farm_land += "<:Crop_Land:753444938791911474>"  # Dirt Emoji
                    continue
                farm_land += CROP_DATA[str(crop.crop_id)]["stages"][crop.state]["emote"]
            farm_land += "\n"
        embed = Embed(title=self.name, description=farm_land)
        return embed
    
    def get_plots(self, planted: bool = True):
        crops = []
        for crop_row, row in enumerate(self.plot):
            for crop_column, crop in enumerate(row):
                if planted and crop != None:
                    crops.append(PlotCoordinate(crop_row, crop_column))
                else:
                    if not planted and crop is None:
                        crops.append(PlotCoordinate(crop_row, crop_column))
        return crops if crops else None

