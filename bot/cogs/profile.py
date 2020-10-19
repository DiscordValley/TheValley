import discord
from discord.ext import commands
from bot.game import Player, Farm
from disputils import BotEmbedPaginator
from typing import List


def divide_chunks(lis, n):
    for i in range(0, len(lis), n):
        yield lis[i : i + n]


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def profile(self, ctx):
        """*Profile command that will show you your stats.*
        **Example**: `{prefix}profile`"""
        player = await Player.load(user_id=ctx.author.id, guild_id=ctx.guild.id)
        farm = await Farm.load(player_id=player.id)
        description = ""
        farm_name = farm.name
        if farm.name is None:
            farm_name = f"{ctx.author.display_name}'s Farm"
        description += f"\n👨‍🌾 **Farm Name:** {farm_name}\n\n **💰 Balance:** {player.balance} \n\n 📊 **Experience:** {player.xp} \n\n 🎚 **Level:** ️{player.level}"

        embed = discord.Embed(
            color=0x336633,
            title=f"{ctx.author.display_name}'s Valley Profile",
            description=description,
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def inventory(self, ctx):
        player = await Player.load(
            user_id=ctx.author.id, guild_id=ctx.guild.id, load_inventory=True
        )
        items = list(player.inventory.items.values())
        if items:
            if len(items) > 5:
                embeds = []
                for p in divide_chunks(items, 5):
                    embeds.append(self.create_inventory_page(ctx, p))
                paginator = BotEmbedPaginator(ctx, embeds)
                await paginator.run()
            else:
                await ctx.send(embed=self.create_inventory_page(ctx, items))
        else:
            embed = discord.Embed(
                title="Inventory", description="Your inventory is empty."
            )
            await ctx.send(embed=embed)

    @staticmethod
    def create_inventory_page(ctx, items: List):
        page = discord.Embed(
            title="Inventory",
        )
        page.set_footer(text=f"Inventory of {ctx.author}")

        for item in items:
            page.add_field(
                name=f"**{item.quantity} {item.name.capitalize()} - {item.cost} coins  **",
                value=item.description,
                inline=False,
            )
        return page


def setup(bot):
    bot.add_cog(Profile(bot))
