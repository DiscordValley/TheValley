import discord
import tweepy
import json
from discord.ext import commands

from bot.utils.constants import COLOR_SUCCESS, COLOR_ERROR

with open("config.json", "r") as f:
    CONFIG = json.load(f)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command(aliases=["t"])
    async def tweet(self, ctx, *, message):
        """*Allows developers to send out tweets easier."""
        auth = tweepy.OAuthHandler(
            CONFIG["TWITTER_API_KEY"], CONFIG["TWITTER_API_SECRET"]
        )
        auth.set_access_token(CONFIG["ACCESS_TOKEN_KEY"], CONFIG["ACCESS_TOKEN_SECRET"])
        api = tweepy.API(auth)

        try:
            if api.update_status(message):
                embed = discord.Embed()
                embed.description = f"Tweet Successful! \n\n Message sent: {message}"
                embed.color = COLOR_SUCCESS
                await ctx.send(embed=embed)
        except tweepy.error.TweepError as e:
            embed = discord.Embed()
            embed.description = f"Tweet Failed! \n\n Error Reason: {e}"
            embed.color = COLOR_ERROR
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))
