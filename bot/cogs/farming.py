import discord
from discord.ext import commands
import re
from typing import List

from bot.game import Farm, Player
from bot.utils.constants import PlotCoordinate, PlotActions, CROP_DATA


PLOT_NOT_FOUND = discord.Embed(
    description="The plot specified was not recognized. Please try again."
)

CROP_NOT_FOUND = discord.Embed(
    description="The crop specified was not recognized. Please try again."
)

NO_AVAILABLE_PLOTS = discord.Emned(
    description="There are no available plots at this time."
)

INSTRUCTIONS = """
        Usage:
            {prefix}[action] <plots>
        <plots> is optional, and can also be multiple arguments.
        """


class Farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def farm(self, ctx):
        player = await Player.load(user_id=ctx.author.id, guild_id=ctx.guild.id)
        farm = await Farm.load(player_id=player.id)
        await ctx.send(embed=farm.display())

    @commands.command(
        brief="*Harvest your crops*", help=INSTRUCTIONS.replace("[action]", "harvest")
    )
    async def harvest(
        self,
        ctx
    ):
        await self.action(
            ctx,
            action=PlotActions.HARVEST,
        )

    @commands.command(
        brief="*Water your crops*", help=INSTRUCTIONS.replace("[action]", "water")
    )
    async def water(
        self,
        ctx
    ):
        valid = True if catcher is None else False
        await self.action(
            ctx,
            action=PlotActions.WATER,
        )

    @commands.command(
        brief="*Plant your crops*", help=INSTRUCTIONS.replace("[action]", "plant")
    )
    async def plant(
        self,
        ctx,
        crop_name: str,
        amount: int
    ):
        valid = True if catcher is None else False
        await self.action(
            ctx,
            action=PlotActions.PLANT,
            crop_name=crop_name,
            amount=amount,
        )

    @staticmethod
    async def action(
        ctx,
        action: PlotActions,
        crop_name: str = None,
        amount: int = None
    ):
        player = await Player.load(user_id=ctx.author.id, guild_id=ctx.guild.id)
        farm = await Farm.load(player_id=player.id)
        coordinates = []
        
        crop_id = None
        if action == PlotActions.PLANT:
            for key, value in CROP_DATA.items():
                if crop_name.casefold() == value.get("name", "invalid").casefold():
                    crop_id = int(key)
                    break
            if crop_id is None:
                return await ctx.send(embed=CROP_NOT_FOUND)
            coordinates = farm.get_plots(planted=False)
            if amount < len(coordinates):
                coordinates = coordinates[:amount]
        else:
            if action == PlotActions.HARVEST or action == PlotActions.WATER:
                coordinates = farm.get_plots(planted=True)

        await farm.work_plots(
            action=action, coordinates=coordinates, crop_id=crop_id
        )

        await ctx.send(embed=farm.display())


def setup(bot):
    bot.add_cog(Farming(bot))
