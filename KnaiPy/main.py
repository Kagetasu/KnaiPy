
from config import token

import discord
from discord.ext import commands

from pathlib import Path

from math import ceil

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='`', intents=intents)

@bot.event
async def setup_hook():
    CMDS_FOLDER = Path('./commands')
    for cmd in CMDS_FOLDER.glob("**/[!_]*.py"):
        await bot.load_extension(cmd.as_posix().removesuffix(".py").replace('/', '.'))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')  
     

@bot.is_owner
@bot.command()
async def reload(ctx, arg):
    try:
        await bot.reload_extension("commands." + arg)
        await ctx.channel.send(embed = discord.Embed(color=0x32a852, title="Extention Reload", description=f"`{arg}` was successfully reloaded"))
    except:
        await ctx.channel.send(embed = discord.Embed(color=0x9c1a36, title="Extention Reload", description=f"Was unnable to reload `{arg}`"))
        raise

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):

    if(isinstance(error, commands.CommandNotFound)):
        return
    
    elif(isinstance(error, commands.errors.CommandOnCooldown)):
        await ctx.reply(f"You are on cooldown, try again in <t:{ceil(ctx.message.created_at.timestamp() + error.retry_after)}:R> ")

    elif(isinstance(error, commands.errors.BadArgument)):
        await ctx.reply(error.args[0])

    elif(isinstance(error, commands.errors.MissingRequiredArgument)):
        await ctx.reply(f"Missing argument: `{error.args[0].split()[0]}`")
        
    else:
        raise error

bot.run(token)




