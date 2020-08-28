import discord
from discord.ext import commands
from enum import Enum
import re
from typing import List


PLOT_NOT_FOUND = discord.Embed(
    description="The plot specified was not recognized. Please try again."
)


class PlotActions(Enum):
    HARVEST = 1
    WATER = 2
    PLANT = 3


class PlotCoordinate:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return f"<{self.row} {self.column}>"


class PlotCoordinateConverter(commands.Converter):
    async def convert(self, ctx, in_coordinate: str):
        match1 = re.match(r"([0-9]+)([A-Za-z]+)", in_coordinate, re.I)
        match2 = re.match(r"([A-Za-z]+)([0-9]+)", in_coordinate, re.I)
        if match1:
            out_coordinate = match1.groups()
            row = int(out_coordinate[0])
            column = out_coordinate[1]
        elif match2:
            out_coordinate = match2.groups()
            column = out_coordinate[0]
            row = int(out_coordinate[1])
        else:
            match1 = re.match(r"[A-Za-z]+", in_coordinate, re.I)
            match2 = re.match(r"\d+", in_coordinate, re.I)
            if match1:
                out_coordinate = match1.group()
                column = out_coordinate[0]
                row = None
            elif match2:
                out_coordinate = match2.group()
                row = int(out_coordinate)
                column = None
            else:
                raise ValueError
        column = ord(column.lower()) - ord("a") + 1 if column else None
        return PlotCoordinate(row, column)


class Farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def harvest(
        self,
        ctx,
        input_coordinates: commands.Greedy[PlotCoordinateConverter],
        *,
        catcher: str = None,
    ):
        """
        *Harvest your crops.*
        Usage:
            {prefix}harvest <plots>
        <plots> is optional, and can also be multiple arguments.
        Rows are enumerated starting at '1'.
        Columns are labeled starting at 'a'.
        Example with 0's instead of plots:
           a   b   c
        1  0   0   0
        2  0   0   0
        3  0   0   0
        <plots> can be a row, column or a specific plot.
        Specific plot is specified by row number followed by column label.
        (for example a1 for the top left plot.)
        If <plots> is not specified, all plots will be harvested.
        """
        farm = self.get_farm()

        if catcher:
            await ctx.send(embed=PLOT_NOT_FOUND)
            return
        else:
            if input_coordinates:
                coordinates = []
                height = len(farm)
                width = len(farm[0])
                for coordinate in input_coordinates:
                    if self.check_plot_validity(farm, coordinate):
                        if coordinate.row and coordinate.column:
                            coordinates.append(coordinate)
                        elif coordinate.row:
                            for i in range(1, width + 1):
                                coordinates.append(
                                    PlotCoordinate(row=coordinate.row, column=i)
                                )
                        elif coordinate.column:
                            for i in range(1, height + 1):
                                coordinates.append(
                                    PlotCoordinate(row=i, column=coordinate.column)
                                )
                    else:
                        await ctx.send(embed=PLOT_NOT_FOUND)
                        return
                farm = self.work_plots(farm, PlotActions.HARVEST, coordinates)
            else:
                farm = self.work_plots(farm, PlotActions.HARVEST)

            await self.display_farm(ctx, farm)

    @commands.command()
    async def water(
        self,
        ctx,
        input_coordinates: commands.Greedy[PlotCoordinateConverter],
        *,
        catcher: str = None,
    ):
        """
        *Water your crops.*
        Usage:
            {prefix}water <plots>
        <plots> is optional, and can also be multiple arguments.
        Rows are enumerated starting at '1'.
        Columns are labeled starting at 'a'.
        Example with 0's instead of plots:
           a   b   c
        1  0   0   0
        2  0   0   0
        3  0   0   0
        <plots> can be a row, column or a specific plot.
        Specific plot is specified by row number followed by column label.
        (for example a1 for the top left plot.)
        If <plots> is not specified, all plots will be watered.
        """
        farm = self.get_farm()

        if catcher:
            await ctx.send(embed=PLOT_NOT_FOUND)
            return
        else:
            if input_coordinates:
                coordinates = []
                height = len(farm)
                width = len(farm[0])
                for coordinate in input_coordinates:
                    if self.check_plot_validity(farm, coordinate):
                        if coordinate.row and coordinate.column:
                            coordinates.append(coordinate)
                        elif coordinate.row:
                            for i in range(1, width + 1):
                                coordinates.append(
                                    PlotCoordinate(row=coordinate.row, column=i)
                                )
                        elif coordinate.column:
                            for i in range(1, height + 1):
                                coordinates.append(
                                    PlotCoordinate(row=i, column=coordinate.column)
                                )
                    else:
                        await ctx.send(embed=PLOT_NOT_FOUND)
                        return
                farm = self.work_plots(farm, PlotActions.WATER, coordinates)
            else:
                farm = self.work_plots(farm, PlotActions.WATER)

            await self.display_farm(ctx, farm)

    @commands.command()
    async def plant(
        self,
        ctx,
        input_coordinates: commands.Greedy[PlotCoordinateConverter],
        *,
        catcher: str = None,
    ):
        """
        *Plant your crops.*
        Usage:
            {prefix}plant <plots>
        <plots> is optional, and can also be multiple arguments.
        Rows are enumerated starting at '1'.
        Columns are labeled starting at 'a'.
        Example with 0's instead of plots:
           a   b   c
        1  0   0   0
        2  0   0   0
        3  0   0   0
        <plots> can be a row, column or a specific plot.
        Specific plot is specified by row number followed by column label.
        (for example a1 for the top left plot.)
        If <plots> is not specified, all plots will be planted.
        """
        farm = self.get_farm()

        if catcher:
            await ctx.send(embed=PLOT_NOT_FOUND)
            return
        else:
            if input_coordinates:
                coordinates = []
                height = len(farm)
                width = len(farm[0])
                for coordinate in input_coordinates:
                    if self.check_plot_validity(farm, coordinate):
                        if coordinate.row and coordinate.column:
                            coordinates.append(coordinate)
                        elif coordinate.row:
                            for i in range(1, width + 1):
                                coordinates.append(
                                    PlotCoordinate(row=coordinate.row, column=i)
                                )
                        elif coordinate.column:
                            for i in range(1, height + 1):
                                coordinates.append(
                                    PlotCoordinate(row=i, column=coordinate.column)
                                )
                    else:
                        await ctx.send(embed=PLOT_NOT_FOUND)
                        return
                farm = self.work_plots(farm, PlotActions.PLANT, coordinates)
            else:
                farm = self.work_plots(farm, PlotActions.PLANT)

            await self.display_farm(ctx, farm)

    @staticmethod
    def check_plot_validity(farm: list, plot):
        len_col = len(farm)
        len_row = len(farm[0])
        if not plot.row and not plot.column:
            return False
        if bool(plot.row):
            if plot.row <= len_col:
                return True
            else:
                return False
        if bool(plot.column):
            if plot.column <= len_row:
                return True
            else:
                return False
        return False

    @staticmethod
    async def display_farm(ctx, farm):
        output_str = ""
        for row in farm:
            for plot in row[:-1]:
                if plot == 1:
                    output_str += str(plot) + "--"
                else:
                    output_str += str(plot) + "-"
            else:
                if row[-1] == 1:
                    output_str += str(row[-1])
                else:
                    output_str += str(row[-1])

            output_str += "\n"
        await ctx.send(
            embed=discord.Embed(title="Current Farm", description=output_str)
        )

    @staticmethod
    def get_farm():
        farm_template = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        return farm_template

    @staticmethod
    def work_plots(farm: list, action: PlotActions, plots: List[PlotCoordinate] = None):
        if action is PlotActions.HARVEST:
            if plots:
                for plot in plots:
                    farm[plot.row - 1][plot.column - 1] = 1
            else:
                for row in farm:
                    for i in range(0, len(row)):
                        row[i] = 1
        elif action is PlotActions.WATER:
            if plots:
                for plot in plots:
                    farm[plot.row - 1][plot.column - 1] = 1
            else:
                for row in farm:
                    for i in range(0, len(row)):
                        row[i] = 1
        elif action is PlotActions.PLANT:
            if plots:
                for plot in plots:
                    farm[plot.row - 1][plot.column - 1] = 1
            else:
                for row in farm:
                    for i in range(0, len(row)):
                        row[i] = 1
        return farm


def setup(bot):
    bot.add_cog(Farming(bot))
