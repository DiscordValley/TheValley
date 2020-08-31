from bot.database.models import Farm as FarmModel
from bot.database.models import PlantedCrop
from bot.game.crop import Crop
from bot.utils.constants import FarmSizes, FARM_SIZE, PlotCoordinate, PlotActions
from typing import List


class Farm:
    def __init__(self, farm_id: int, size: FarmSizes, name: str):
        self.id = farm_id
        self.name = name
        self.size = size
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

    def initialize_plot(self) -> List[List[Crop]]:
        size = FARM_SIZE.get(self.size)
        return [[None] * size.rows] * size.columns

    async def load_crops(self):
        crops = await PlantedCrop.query.where(FarmModel.id == self.id).gino.all()
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
        size = FARM_SIZE.get(self.size)
        if row is not None:
            if row >= size.rows or row < 0:
                return False
        if column is not None:
            if column >= size.columns or column < 0:
                return False
        return True

    def place_crop(self, crop: Crop, row: int, column: int):
        if not self.validate_coordinate(row=row, column=column):
            raise ValueError("Crop placement out of bounds")
        self.plot[row][column] = crop

    async def work_plot(self, action: PlotActions, row: int, column: int):
        if not self.validate_coordinate(row, column):
            return
        if self.plot[row][column] is not None:
            self.plot[row][column].work(action)
        else:
            if action is PlotActions.PLANT:
                self.plot[row][column] = await Crop.new(
                    farm_id=self.id, crop_id=1
                )  # TODO: Plant kinda needs some crop_id passed doesn't it?

    async def work_plots(self, action: PlotActions, coordinates: List[PlotCoordinate]):
        size = FarmSizes.get(self.size)
        if not coordinates:
            for row in range(size.rows):
                for column in range(size.columns):
                    await self.work_plot(action=action, row=row, column=column)

        for coordinate in coordinates:
            if coordinate.row is None and coordinate.column is not None:
                for row in range(size.rows):
                    await self.work_plot(
                        action=action, row=row, column=coordinate.column
                    )
            elif coordinate.column is None and coordinate.row is not None:
                for column in range(size.columns):
                    await self.work_plot(
                        action=action, row=coordinate.row, column=column
                    )

    def display(self):
        # TODO: representation logic
        return self.plot
