import discord
from discord.ext import commands
from bot.game import Player


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command(aliases=["leader", "lead", "board", "top"])
    async def leaderboard(self, ctx):
        """*Leaderboard command. This will show *
        **Example**: `{prefix}`leaderboard"""

        leader = await Player.top(guild_id=ctx.guild.id)
        embed = discord.Embed(
            title="The Valley Leader Board",
            description="Below are the top players in The Valley! " "Worship them!",
        )
        embed.add_field(name="<@" + str(leader[0].id) + ">", value=leader[0].xp)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Leaderboard(bot))
