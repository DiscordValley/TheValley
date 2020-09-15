import discord
import json

from discord.ext import commands
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from datetime import datetime

with open("shop.json", "r") as f:
    data = json.load(f)


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

        seeds = data["seeds"]
        seed_json = [
            (product["name"], product["price"], product["stock"], product["item_id"])
            for product in seeds
        ]

        tool = data["tools"]
        tool_json = [
            (tools["name"], tools["price"], tools["item_id"]) for tools in tool
        ]

        IOTD = data["iotd"]
        iotd_json = [(spec["name"], spec["price"], spec["item_id"]) for spec in IOTD]

        descriptionSeeds = ""
        for item in seed_json:
            descriptionSeeds += f"**{seed_json.index(item) + 1}.** {item[0]} **|** {item[1]} **|** {item[2]} **|** {item[3]}\n"

        descriptionTools = ""
        for item in tool_json:
            descriptionTools += f"**{tool_json.index(item) + 1}.** {item[0]} **|** {item[1]} **|** {item[2]}\n"

        descriptionIOTD = ""
        for item in iotd_json:
            descriptionIOTD += f"**{iotd_json.index(item) + 1}.** {item[0]} **|** {item[1]} **|** {item[2]}\n"
        embeds = [
            discord.Embed(
                title="Seed Store", description=descriptionSeeds, color=0x115599
            ),
            discord.Embed(
                title="Tool Store", description=descriptionTools, color=0x115599
            ),
            discord.Embed(
                title="Item Of The Day", description=descriptionIOTD, color=0x115599
            ),
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()


def setup(bot):
    bot.add_cog(Store(bot))
