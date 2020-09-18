import sys
import time
from datetime import datetime

import discord
from discord.ext import commands

from bot import utils

from disputils import BotEmbedPaginator


PY_VERSION = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)

COMMAND_NOT_FOUND = discord.Embed(
    description="The command specified was not recognized. Please try again."
)


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now().replace(microsecond=0)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def ping(self, ctx):
        """*Current ping and latency of the bot*
        **Example**: `{prefix}ping`"""
        embed = discord.Embed()
        before_time = time.time()
        msg = await ctx.send(embed=embed)
        latency = round(self.bot.latency * 1000)
        elapsed_ms = round((time.time() - before_time) * 1000) - latency
        embed.add_field(name="ping", value=f"{elapsed_ms}ms")
        embed.add_field(name="latency", value=f"{latency}ms")
        await msg.edit(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        """*Current uptime of the bot*
        **Example**: `{prefix}uptime`"""
        current_time = datetime.now().replace(microsecond=0)
        embed = discord.Embed(
            description=f"Time since I went online: {current_time - self.start_time}."
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def starttime(self, ctx):
        """*When the bot was started*
        **Example**: `{prefix}starttime`"""
        embed = discord.Embed(description=f"I'm up since {self.start_time}.")
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        """*Shows stats and infos about the bot*
        **Example**: `{prefix}info`"""
        embed = discord.Embed(title="Daisy")
        # embed.url = f"https://top.gg/bot/{self.bot.user.id}"
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name="Bot Stats",
            value=f"```py\n"
            f"Guilds: {len(self.bot.guilds)}\n"
            f"Users: {len(self.bot.users)}\n"
            f"Shards: {self.bot.shard_count}\n"
            f"Shard ID: {ctx.guild.shard_id}```",
            inline=False,
        )
        embed.add_field(
            name="Server Configuration",
            value=f"```\n" f"Prefix: {utils.config.prefix}\n" f"```",
            inline=False,
        )
        embed.add_field(
            name="Software Versions",
            value=f"```py\n"
            f"Daisy: {self.bot.version}\n"
            f"discord.py: {discord.__version__}\n"
            f"Python: {PY_VERSION}```",
            inline=False,
        )
        embed.add_field(
            name="Links",
            value=f"[Invite]({self.bot.invite})",
            inline=False,
        )
        embed.set_footer(
            text="Thank you for using DiscordValley <3",
            icon_url=self.bot.user.avatar_url,
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["socials", "links", "support"])
    async def invite(self, ctx):
        """*Shows invite link and other socials for the bot*
        **Aliases**: `socials`, `links`, `support`
        **Example**: `{prefix}invite`"""
        embed = discord.Embed()
        embed.description = f"[Invite]({self.bot.invite})"
        embed.set_footer(
            text="Thank you for using DiscordValley <3",
            icon_url=self.bot.user.avatar_url,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, command_name: str = None):
        """*Shows this message*"""
        prefix = utils.get_guild_prefix(self.bot, ctx.guild.id)
        if command_name is None:
            embeds = []
            for cog in self.bot.cogs:
                embed = discord.Embed(title=cog)
                for command in self.bot.get_cog(cog).get_commands():
                    brief = command.short_doc
                    if brief is False:
                        brief = "Command brief not found not"
                    if command.hidden:
                        continue
                    embed.add_field(
                        name=f"{prefix}{command.name}", value=brief, inline=False
                    )
                embeds.append(embed)
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
            return
        command = self.bot.get_command(command_name.casefold())
        if command is None:
            await ctx.send(embed=COMMAND_NOT_FOUND)
            return
        embed = discord.Embed(
            title=f"{prefix}{command.name}",
            description=f"```{command.help.format(prefix=prefix)}```",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
