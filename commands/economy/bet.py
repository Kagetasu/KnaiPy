from discord.ext import commands

from random import random, uniform
from math import floor

from utils import MoneyConverterType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.economy import Database


@commands.command()
async def bet(ctx: commands.Context, amnt: MoneyConverterType):
    db: "Database" = ctx.bot.db

    if random() >= 0.55:
        win = floor(uniform(0.3, 0.5) * amnt)
        await ctx.send(f"Congrats! You won **${win}**!")
        await db.update(ctx.author.id, "+", win)
    else:
        await ctx.send("You lost 😝")
        await db.update(ctx.author.id, "-", amnt)


async def setup(bot):
    bot.add_command(bet)
