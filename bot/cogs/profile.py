import discord
from discord.ext import commands
from bot.game import Player, Farm, InventoryItem
from disputils import BotEmbedPaginator
from typing import List
from operator import attrgetter


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
    async def inventory(self, ctx, criteria: str = None, order: str = None):
        """*Inventory command that will show your inventory.*
        **Example**: `{prefix}inventory`"""
        player = await Player.load(
            user_id=ctx.author.id, guild_id=ctx.guild.id, load_inventory=True
        )
        sorting = ["lowest", "highest"]
        items = list(player.inventory.items.values())
        if criteria:
            high_aliases = ["high", "h", "top", "hi"]
            low_aliases = ["low", "l", "bottom", "lo"]
            if order:
                if order in high_aliases:
                    sorting.reverse()
                    items = self.sort_items(items, criteria, True)
                elif order in low_aliases:
                    items = self.sort_items(items, criteria, False)
                else:
                    embed = discord.Embed(
                        description="The order was not recognised. Please try again."
                    )
                    await ctx.send(embed=embed)
                    return
            else:
                items = self.sort_items(items, criteria, False)
        if items:
            if len(items) > 5:
                embeds = []
                for p in divide_chunks(items, 5):
                    embeds.append(self.create_inventory_page(ctx, p, sorting))
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
    def create_inventory_page(ctx, items: List, sorting: List[str] = None):
        if sorting:
            page = discord.Embed(
                description=f"Sorting from {sorting[0]} to {sorting[1]}."
            )
        else:
            page = discord.Embed()
        page.set_footer(text=f"Inventory of {ctx.author}")

        for item in items:
            page.add_field(
                name=f"**{item.quantity} {item.name.capitalize()} - {item.cost} coins  **",
                value=item.description,
                inline=False,
            )
        return page

    @staticmethod
    def sort_items(items: List, criteria: str, reverse: bool):
        if criteria == "value":
            return sorted(items, key=attrgetter("cost"), reverse=reverse)
        elif criteria == "amount":
            return sorted(items, key=lambda item: item.quantity, reverse=reverse)
        else:
            return None


def setup(bot):
    bot.add_cog(Profile(bot))
