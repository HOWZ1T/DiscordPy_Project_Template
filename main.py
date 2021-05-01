from os import listdir, environ
from os.path import isfile, join
from discord.ext import commands
from logging import StreamHandler
from dotenv import dotenv_values

import discord.ext.commands.view
import discord
import sys
import traceback
import logging

# load config from dot env file
config = None
if "PYCHARM_HOSTED" in environ:
    config = dotenv_values("./envs/.env.dev")
else:
    config = dotenv_values("./envs/.env.prod")

# setup logging
logging_handlers = [StreamHandler(stream=sys.stdout)]
if "PYCHARM_HOSTED" in environ:
    logging.basicConfig(
        format="%(asctime)s Bot: | %(name)20s | %(funcName)20s() | %(levelname)8s | %(message)s",
        datefmt="%b %d %H:%M:%S",
        level=logging.DEBUG,
        handlers=logging_handlers
    )
else:
    logging.basicConfig(
        format="%(asctime)s Bot: | %(name)20s | %(funcName)20s() | %(levelname)8s | %(message)s",
        datefmt="%b %d %H:%M:%S",
        level=logging.ERROR,
        handlers=logging_handlers
    )
log = logging.getLogger(__name__)

# silence discord and websockets
logging.getLogger("discord.client").setLevel(logging.ERROR)
logging.getLogger('discord.gateway').setLevel(logging.ERROR)
logging.getLogger("discord.state").setLevel(logging.ERROR)
logging.getLogger("discord.http").setLevel(logging.ERROR)
logging.getLogger("websockets.protocol").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("datapipelines.pipelines").setLevel(logging.WARNING)

cogs_dir = "cogs"
bot = commands.Bot(command_prefix=config["prefix"], description=config["description"])

# load cogs from cogs dir, cogs are logical groupings of code for executing commands and/or listening to events
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()


@bot.event
async def on_ready():
    # event triggered when bot is logged in and ready
    log.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    log.info(f'Version: {discord.__version__}\n')


@bot.event
async def on_command_error(ctx, error):
    # event triggered when a command error occurs
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: Try {ctx.prefix}help {ctx.command}")


# runs the bot
bot.run(config["token"], bot=True, reconnect=True)
