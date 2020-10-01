from typing import Union

import discord
import json

from discord.ext import commands
from disputils import BotEmbedPaginator, BotConfirmation

from bot.game import Player, Item

from bot.utils.constants import COLOR_ERROR, COLOR_SUCCESS, COLOR_INFO

with open("shop.json", "r") as f:
    SHOPS_DATA = json.load(f)


class Store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.group(invoke_without_command=True, pass_context=True)
    async def store(self, ctx):
        """*Store command of bot. Will show static seeds for now.*
        **Example**: `{prefix}store`"""

        seeds = SHOPS_DATA.get("seeds", [])
        seed_descriptions = ""
        for index, product in enumerate(seeds):
            try:
                name = product["name"]
                price = product["price"]
                stock = product["stock"]
                item_id = product["item_id"]

                seed_descriptions += f"**{index + 1}.** {name} (*{item_id}*) **|** {price} **|** {stock}\n"
            except KeyError:
                continue

        tools = SHOPS_DATA.get("tools", [])
        tool_descriptions = ""
        for index, tool in enumerate(tools):
            try:
                name = tool["name"]
                price = tool["price"]
                item_id = tool["item_id"]

                tool_descriptions += (
                    f"**{index + 1}.** {name} (*{item_id}*) **|** {price}\n"
                )
            except KeyError:
                continue

        iotd = SHOPS_DATA.get("iotd", [])
        iotd_descriptions = ""
        for index, item in enumerate(iotd):
            try:
                name = item["name"]
                price = item["price"]
                item_id = item["item_id"]
                desc = item["description"]

                iotd_descriptions += (
                    f"**Name: {name}** *{item_id}*\n **{price}** \n {desc}"
                )
            except KeyError:
                continue

        embeds = [
            discord.Embed(
                title="Seed Store", description=seed_descriptions, color=0x115599
            ),
            discord.Embed(
                title="Tool Store", description=tool_descriptions, color=0x115599
            ),
            discord.Embed(
                title="Item Of The Day", description=iotd_descriptions, color=0x115599
            ),
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

    @store.command(aliases=["details", "info", "desc"])
    async def description(self, ctx, *, name: str):
        """*Description of items in store. Use item name.*
        **Example**: `{prefix}store desc Parsnips`"""
        item_obj = await Item.item(name=name)
        print(item_obj)
        desc_embed = discord.Embed(
            description=f"***Item Name:***  {item_obj.name}\n***Item ID:***  {item_obj.id}\n***Item Description:***  {item_obj.description}\n***Item Cost:***  {item_obj.cost}"
            f"\n***Item Creation ID:***  {item_obj.creation_id}"
        )
        desc_embed.color = COLOR_INFO
        await ctx.send(embed=desc_embed)

    @store.command()
    async def sell(self, ctx, name: str, quantity: Union[int, str]):
        if isinstance(quantity, int) and quantity <= 0:
            embed_fail = discord.Embed(
                description=f"Please enter a number or full number for quantity. You entered: `{quantity}`",
            )
            embed_fail.color = COLOR_ERROR
            await ctx.send(embed=embed_fail)
            return

        player, player_obj = await Player.load(
            user_id=ctx.author.id, guild_id=ctx.guild.id, db_object=True
        )
        item_obj = await Item.load(name=name)
        inv_obj, quantity = await Player.validate_sell(
            item_id=item_obj.id, player_id=player.id, quantity=quantity
        )
        if inv_obj is None:
            embed_fail = discord.Embed(
                description=f"Item not found in inventory. Enter an item that you have in your inventory.: `{name}`",
            )
            embed_fail.color = COLOR_ERROR
            await ctx.send(embed=embed_fail)
            return
        if inv_obj.quantity == quantity:
            confirmation = BotConfirmation(ctx, COLOR_INFO)
            await confirmation.confirm(
                f"You are trying to sell all of your item: `{item_obj.name}`. Are you sure?"
            )

            if confirmation.confirmed:
                await confirmation.update("Confirmed", color=COLOR_SUCCESS)
            else:
                await confirmation.update(
                    "Not confirmed, sale aborted.", hide_author=True, color=COLOR_ERROR
                )
                return
        price, balance = await Player.sell(
            player_obj=player_obj, item_obj=item_obj, inv_obj=inv_obj, quantity=quantity
        )
        embed_suc = discord.Embed(
            description=f"Success! You sold `{quantity}` of `{item_obj.name}` for `{price}`. \n\n"
            f"You now have a total of `{balance}` coins"
        )
        embed_suc.color = COLOR_SUCCESS
        await ctx.send(embed=embed_suc)

    @store.command()
    async def buy(self, ctx, name: str, quantity: int):
        player = await Player.load(user_id=ctx.author.id, guild_id=ctx.guild.id)

        return


def setup(bot):
    bot.add_cog(Store(bot))
