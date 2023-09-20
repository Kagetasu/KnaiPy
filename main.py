import discord
from discord.ext import commands

from pathlib import Path

from utils.economy import Database
from config import token

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="`",
    intents=intents,
)


@bot.event
async def setup_hook():
    bot.db = Database()  # type: ignore

    CMDS_FOLDER = Path("./commands")
    for cmd in CMDS_FOLDER.glob("**/[!_]*.py"):
        await bot.load_extension(cmd.as_posix().removesuffix(".py").replace("/", "."))

    print(f"Logged in as {bot.user}")


bot.run(token)
