import discord
import json

from discord.ext import commands
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from datetime import datetime

with open("shop.json", "r") as f:
    SHOPS_DATA = json.load(f)


class Store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
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
                    f"**{index +1}.** {name} (*{item_id}*) **|** {price}\n"
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


def setup(bot):
    bot.add_cog(Store(bot))
