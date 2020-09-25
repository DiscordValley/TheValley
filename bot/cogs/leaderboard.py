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
        # Made by 375009157012520966 only him, he only wrote this, he is great
        board = [
            (self.bot.get_user(player.user_id), player.level, player.xp)
            for player in await Player.top(guild_id=ctx.guild.id)
        ]
        description = ""
        # user1 = bot.get_user(leader[0].id)
        for user in board:
            description += f"**{board.index(user) + 1}.** {user[0].mention} | Level: {user[1]} | XP: {user[2]}\n"
        msg = discord.Embed(
            color=discord.Color.green(),
            title=f"{str(ctx.guild)}" "s Valley Leaderboard",
            description=description,
        )

        await ctx.send(embed=msg)


def setup(bot):
    bot.add_cog(Leaderboard(bot))
