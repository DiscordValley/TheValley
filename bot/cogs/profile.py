import discord
from discord.ext import commands
from bot.game import Player, Farm


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
        embed.add_field(name="Balance", value=player.balance)
        embed.add_field(name="XP", value=player.xp)
        embed.add_field(name="Level", value=player.level)
        await ctx.send(embed=embed)

    @commands.command()
    async def inventory(self, ctx):
        player = await Player.load(
            user_id=ctx.author.id, guild_id=ctx.guild.id, load_inventory=True
        )
        embed = discord.Embed(title="Inventory")
        embed.set_footer(text=f"Inventory of {ctx.author}")
        for item in player.inventory.items:
            embed.add_field(name=item.name.capitalize(), value=str(item.quantity))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
