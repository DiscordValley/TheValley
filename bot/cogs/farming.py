import discord
from discord.ext import commands
import re
from typing import List

from bot.game import Farm, Player
from bot.utils.constants import PlotCoordinate, PlotActions


PLOT_NOT_FOUND = discord.Embed(
    description="The plot specified was not recognized. Please try again."
)

INSTRUCTIONS = """
        Usage:
            {prefix}[action] <plots>
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
        If <plots> is not specified, all plots will be [action]ed.
        """


class PlotCoordinateConverter(commands.Converter):
    async def convert(self, ctx, in_coordinate: str):
        match_1a = re.match(r"([0-9]+)([A-Za-z]+)", in_coordinate, re.I)
        match_a1 = re.match(r"([A-Za-z]+)([0-9]+)", in_coordinate, re.I)
        if match_1a:
            out_coordinate = match_1a.groups()
            row = int(out_coordinate[0])
            column = out_coordinate[1]
        elif match_a1:
            out_coordinate = match_a1.groups()
            column = out_coordinate[0]
            row = int(out_coordinate[1])
        else:
            match_a = re.match(r"[A-Za-z]+", in_coordinate, re.I)
            match_1 = re.match(r"\d+", in_coordinate, re.I)
            if match_a:
                out_coordinate = match_a.group()
                column = out_coordinate[0]
                row = None
            elif match_1:
                out_coordinate = match_1.group()
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

    @commands.command(
        brief="*Harvest your crops*", help=INSTRUCTIONS.replace("[action]", "harvest")
    )
    async def harvest(
        self,
        ctx,
        input_coordinates: commands.Greedy[PlotCoordinateConverter],
        *,
        catcher: str = None,
    ):
        valid = True if catcher is None else False
        await self.action(
            ctx,
            input_coordinates,
            action=PlotActions.HARVEST,
            valid=valid,
        )

    @commands.command(
        brief="*Water your crops*", help=INSTRUCTIONS.replace("[action]", "water")
    )
    async def water(
        self,
        ctx,
        input_coordinates: commands.Greedy[PlotCoordinateConverter],
        *,
        catcher: str = None,
    ):
        valid = True if catcher is None else False
        await self.action(
            ctx,
            input_coordinates,
            action=PlotActions.WATER,
            valid=valid,
        )

    @commands.command(
        brief="*Plant your crops*", help=INSTRUCTIONS.replace("[action]", "plant")
    )
    async def plant(
        self,
        ctx,
        input_coordinates: commands.Greedy[PlotCoordinateConverter],
        *,
        catcher: str = None,
    ):
        valid = True if catcher is None else False
        await self.action(
            ctx,
            input_coordinates,
            action=PlotActions.PLANT,
            valid=valid,
        )

    @staticmethod
    async def action(
        self,
        ctx,
        input_coordinates: List[PlotCoordinate],
        action: PlotActions,
        valid: bool = True,
    ):
        if not valid:
            return await ctx.send(embed=PLOT_NOT_FOUND)

        player = await Player.load(user_id=ctx.author.id, guild_id=ctx.guild.id)
        farm = await Farm.load(player_id=player.id)

        if input_coordinates:
            for coordinate in input_coordinates:
                if not farm.validate_coordinate(
                    row=coordinate.row, column=coordinate.column
                ):
                    return await ctx.send(embed=PLOT_NOT_FOUND)

        await farm.work_plots(action=action, coordinates=input_coordinates)

        await ctx.send(farm.display())


def setup(bot):
    bot.add_cog(Farming(bot))
