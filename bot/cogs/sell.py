import discord
import json

from discord.ext import commands

from bot.game import Player
from bot.utils import constants
from disputils import BotConfirmation

from bot.utils.constants import COLOR_ERROR, COLOR_SUCCESS


class Sell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def sell(self, ctx, item, quantity):
        """*Sell command of bot. This command is used for selling an item that a player has in their inventory.
        If a user has no input after name, it will always sell one of the item.*
                **Example**: `{prefix}sell <<item ID or name>> <<quantity>>`"""
        player = await Player.load(user_id=ctx.author.id, guild_id=ctx.guild.id)
        # sellObj = await Player.sell(item_id=item, player_id=player.id)
        itemObj = await Player.item(item_id=item)
        print(itemObj)
        try:
            quantityNum = int(quantity)
            # sellObj.update(quantity=quantity)
            await ctx.send(itemObj)
            embedSuc = discord.Embed(
                description='Success! You sold `{}` of `{}`'.format(quantityNum, item),
            )
            embedSuc.color = COLOR_SUCCESS
            await ctx.send(embed=embedSuc)
        except ValueError:
            embedFail = discord.Embed(
                description='Please enter a number or full number for quantity. You entered: `{}`'.format(quantity),
            )
            embedFail.color = COLOR_ERROR
            await ctx.send(embed=embedFail)

        # await ctx.send('Item: {}\nQuantity: {}'.format(item, quantity))


def setup(bot):
    bot.add_cog(Sell(bot))
