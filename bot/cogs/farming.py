import discord
from discord.ext import commands
from enum import Enum
import re


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
    async def convert(self, ctx, argument: str):
        match1 = re.match(r"([0-9]+)([A-Za-z]+)", argument, re.I)
        match2 = re.match(r"([A-Za-z]+)([0-9]+)", argument, re.I)
        if match1:
            rc_list = match1.groups()
            row = int(rc_list[0])
            column = rc_list[1]
        elif match2:
            rc_list = match2.groups()
            column = rc_list[0]
            row = int(rc_list[1])
        else:
            match1 = re.match(r"[A-Za-z]+", argument, re.I)
            match2 = re.match(r"\d+", argument, re.I)
            if match1:
                rc_list = match1.group()
                column = rc_list[0]
                row = None
            elif match2:
                rc_list = match2.group()
                row = int(rc_list)
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
    async def harvest(self, ctx, plots: commands.Greedy[PlotCoordinateConverter]):
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
        farm_template = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        if plots:
            rc_list = plots
            len_col = len(farm_template)
            len_row = len(farm_template[0])

            for rc in rc_list:
                if not self.check_plot_validity(farm_template, rc):
                    await ctx.send(embed=PLOT_NOT_FOUND)
                    return
            for rc in rc_list:
                if rc.row and rc.column:
                    # Should be function which harvests a single plot.
                    farm_template[rc.row - 1][rc.column - 1] = 1
                elif rc.row:
                    for i in range(len_row):
                        # Should be function which harvests a single plot.
                        farm_template[rc.row - 1][i] = 1
                else:
                    for i in range(len_col):
                        # Should be function which harvests a single plot.
                        farm_template[i][rc.column - 1] = 1
        else:
            for row in farm_template:
                for i in range(0, len(row)):
                    # Should be function which harvests a single plot.
                    row[i] = 1
        output_str = ""
        # Show
        for row in farm_template:
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

    @commands.command()
    async def water(self, ctx, plots: commands.Greedy[PlotCoordinateConverter]):
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
        farm_template = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        if plots:
            rc_list = plots
            len_col = len(farm_template)
            len_row = len(farm_template[0])

            for rc in rc_list:
                if not self.check_plot_validity(farm_template, rc):
                    await ctx.send(embed=PLOT_NOT_FOUND)
                    return
            for rc in rc_list:
                if rc.row and rc.column:
                    # Should be function which harvests a single plot.
                    farm_template[rc.row - 1][rc.column - 1] = 1
                elif rc.row:
                    for i in range(len_row):
                        # Should be function which harvests a single plot.
                        farm_template[rc.row - 1][i] = 1
                else:
                    for i in range(len_col):
                        # Should be function which harvests a single plot.
                        farm_template[i][rc.column - 1] = 1
        else:
            for row in farm_template:
                for i in range(0, len(row)):
                    # Should be function which harvests a single plot.
                    row[i] = 1
        output_str = ""
        # Show
        for row in farm_template:
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

    @commands.command()
    async def plant(self, ctx, plots: commands.Greedy[PlotCoordinateConverter]):
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
        farm_template = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        if plots:
            rc_list = plots
            len_col = len(farm_template)
            len_row = len(farm_template[0])

            for rc in rc_list:
                if not self.check_plot_validity(farm_template, rc):
                    await ctx.send(embed=PLOT_NOT_FOUND)
                    return
            for rc in rc_list:
                if rc.row and rc.column:
                    # Should be function which harvests a single plot.
                    farm_template[rc.row - 1][rc.column - 1] = 1
                elif rc.row:
                    for i in range(len_row):
                        # Should be function which harvests a single plot.
                        farm_template[rc.row - 1][i] = 1
                else:
                    for i in range(len_col):
                        # Should be function which harvests a single plot.
                        farm_template[i][rc.column - 1] = 1
        else:
            for row in farm_template:
                for i in range(0, len(row)):
                    # Should be function which harvests a single plot.
                    row[i] = 1
        output_str = ""
        # Show
        for row in farm_template:
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
    def check_plot_validity(farm: list, plot):
        len_col = len(farm)
        len_row = len(farm[0])

        if not plot.row and not plot.column:
            return False
        if plot.row:
            if plot.row > len_col:
                return False
        if plot.column:
            if plot.column > len_row:
                return False
        return True


def setup(bot):
    bot.add_cog(Farming(bot))
