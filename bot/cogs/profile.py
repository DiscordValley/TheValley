import discord
from discord.ext import commands
from bot.game import Player, Farm
from disputils import BotEmbedPaginator


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
        embed = discord.Embed(
            title="Your Valley Profile",
            description="This command will show you where you are in "
            "terms of ranking, and other information about "
            "your account.",
        )
        embed.add_field(name="Farm Name", value=farm.name)
        embed.add_field(name="Balance", value=str(player.balance))
        embed.add_field(name="XP", value=str(player.xp))
        embed.add_field(name="Level", value=str(player.level))
        await ctx.send(embed=embed)

    @commands.command()
    async def inventory(self, ctx):
        player = await Player.load(
            user_id=ctx.author.id, guild_id=ctx.guild.id, load_inventory=True
        )
        items = player.inventory.items.values()

        if items:
            if len(items) > 5:
                pages = list(divide_chunks(list(items), 5))
                embeds = []
                for p in pages:
                    embed = discord.Embed(
                        title="Inventory",
                    )
                    embed.set_footer(text=f"Inventory of {ctx.author}")

                    for item in p:
                        embed.add_field(
                            name=f"**{item.quantity} - {item.name.capitalize()} - {item.cost}**",
                            value=item.description,
                            inline=False,
                        )
                    embeds.append(embed)
                paginator = BotEmbedPaginator(ctx, embeds)
                await paginator.run()
            else:
                embed = discord.Embed(
                    title="Inventory",
                )
                embed.set_footer(text=f"Inventory of {ctx.author}")
                print("there has been a mistake")
                for item in items:
                    embed.add_field(
                        name=f"**{item.quantity} - {item.name.capitalize()} - {item.cost}**",
                        value=item.description,
                        inline=False,
                    )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Inventory", description="Your inventory is empty."
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
