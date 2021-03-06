from pathlib import Path

import discord
from discord.ext import commands

from bot import utils, database
from bot.database.models import Guild

__version__ = "0.1.0"

invite_link = (
    "https://discordapp.com/api/oauth2/authorize?client_id={}&scope=bot&permissions=0"
)


async def get_prefix(_bot, message):
    prefix = utils.config.prefix
    if not isinstance(message.channel, discord.DMChannel):
        prefix = utils.get_guild_prefix(_bot, message.guild.id)
    return commands.when_mentioned_or(prefix)(_bot, message)


bot = commands.AutoShardedBot(command_prefix=get_prefix)
bot.version = __version__
bot.guild_data = {}


async def preload_guild_data():
    guilds = await Guild.query.gino.all()
    d = dict()
    for guild in guilds:
        d[guild.id] = {"prefix": guild.prefix}
    return d


@bot.event
async def on_ready():
    bot.invite = invite_link.format(bot.user.id)
    await database.setup()
    bot.guild_data = await preload_guild_data()
    print(
        f"""Logged in as {bot.user}..
        Serving {len(bot.users)} users in {len(bot.guilds)} guilds
        Invite: {invite_link.format(bot.user.id)}
    """
    )


@bot.event
async def on_command_error(ctx, error):
    prefix = utils.get_guild_prefix(bot, ctx.guild.id)
    embed = discord.Embed()
    if isinstance(error, commands.MissingRequiredArgument):
        embed.description = f"⚠️ Missing some required arguments.\n\nPlease use `{prefix}help` for more info!"
    elif hasattr(error, "original"):
        if isinstance(error.original, utils.errors.ItemNotFoundError):
            embed.description = (
                f"⚠️ Item `{error.original.item}` not found.\n "
                f"Please try again with an actual item. Thanks!"
            )
        elif isinstance(error.original, utils.errors.InvalidQuantityError):
            embed.description = f"⚠️ `{error.original.name}` is an invalid argument. Please enter a number or `all`"
        else:
            raise error
    else:
        raise error
    await ctx.send(embed=embed)


def extensions():
    files = Path("bot", "cogs").rglob("*.py")
    for file in files:
        yield file.as_posix()[:-3].replace("/", ".")


def load_extensions(_bot):
    for ext in extensions():
        try:
            _bot.load_extension(ext)
        except Exception as ex:
            print(f"Failed to load extension {ext} - exception: {ex}")


def run():
    load_extensions(bot)
    bot.run(utils.config.token)
