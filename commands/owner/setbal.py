from discord import User
from discord.ext import commands

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.economy import Database


@commands.is_owner()
@commands.command(aliases=["setb"])
async def setbal(ctx: commands.Context, user: User, amnt: float):
    db: "Database" = ctx.bot.db
    await db.update(user.id, "set", amnt=amnt)
    await ctx.reply(f"Updated balance for <@{user.id}> ✅")


async def setup(bot):
    bot.add_command(setbal)
