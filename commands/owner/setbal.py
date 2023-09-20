from discord import User
from discord.ext import commands

from databases.economydb import update

@commands.is_owner()
@commands.command(aliases = ["setb"])
async def setbal(ctx: commands.Context, user: User, amnt: float):

    update(user.id, 'set', amnt=amnt)
    await ctx.reply(f"Updated balance for <@{user.id}> ✅")

async def setup(bot):
    bot.add_command(setbal)