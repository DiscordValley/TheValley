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

    async def work_plots(self, action: PlotActions, coordinates: List[PlotCoordinate]):
        # if action is PlotActions.HARVEST:
        #     if plots:
        #         for plot in plots:
        #             farm[plot.row - 1][plot.column - 1] = 1
        #     else:
        #         for row in farm:
        #             for i in range(0, len(row)):
        #                 row[i] = 1
        # elif action is PlotActions.WATER:
        #     if plots:
        #         for plot in plots:
        #             farm[plot.row - 1][plot.column - 1] = 1
        #     else:
        #         for row in farm:
        #             for i in range(0, len(row)):
        #                 row[i] = 1
        # elif action is PlotActions.PLANT:
        #     if plots:
        #         for plot in plots:
        #             farm[plot.row - 1][plot.column - 1] = 1
        #     else:
        #         for row in farm:
        #             for i in range(0, len(row)):
        #                 row[i] = 1
        pass

    def display(self):
        # output_str = ""
        # for row in farm:
        #     for plot in row[:-1]:
        #         if plot == 1:
        #             output_str += str(plot) + "--"
        #         else:
        #             output_str += str(plot) + "-"
        #     else:
        #         if row[-1] == 1:
        #             output_str += str(row[-1])
        #         else:
        #             output_str += str(row[-1])
        #
        #     output_str += "\n"
        return self.plot
