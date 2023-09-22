import discord
from discord.ext import commands

from math import ceil


async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return

    elif isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.reply(
            f"You are on cooldown, try again in <t:{ceil(ctx.message.created_at.timestamp() + error.retry_after)}:R> "
        )

    elif isinstance(error, commands.errors.BadArgument):
        await ctx.reply(error.args[0])

    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(f"Missing argument: `{error.args[0].split()[0]}`")

    else:
        raise error


async def setup(bot: commands.Bot):
    bot.add_listener(on_command_error, "on_command_error")
