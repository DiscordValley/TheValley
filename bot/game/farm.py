from bot.database.models import Farm as FarmModel
from bot.database.models import Plant as PlantModel
from bot.game.plant import Plant
from bot.utils.constants import FarmSizes, FARM_SIZE
from typing import List


class Farm:
    def __init__(self, farm_id: int, size: FarmSizes, name: str):
        self.id = farm_id
        self.name = name
        self.size = size
        self.plot = self.initialize_plot()

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

    def initialize_plot(self) -> List[List[Plant]]:
        size = FARM_SIZE.get(self.size)
        return [[None] * size.rows] * size.columns

    async def load_crops(self):
        plants = await PlantModel.query.where(FarmModel.id == self.id).gino.all()
        for plant in plants:
            self.place_crop(
                Plant(
                    id=plant.id,
                    farm_id=plant.farm_id,
                    crop_id=plant.crop_id,
                    planted_at=plant.planted_at,
                ),
                row=plant.coord_row,
                column=plant.coord_column,
            )

    def place_crop(self, crop: Plant, row: int, column: int):
        size = FARM_SIZE.get(self.size)
        if row >= size.rows or column >= size.columns or row < 0 or column < 0:
            raise ValueError("Crop placement out of bounds.")
        self.plot[row][column] = crop
