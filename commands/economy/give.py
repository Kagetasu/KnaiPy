import discord
from discord.ext import commands

from utils import Embed, MoneyConverterType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.economy import Database


@commands.command()
async def give(ctx: commands.Context, user: discord.User, amnt: MoneyConverterType):
    if user.id == ctx.author.id:
        return await ctx.reply(f"Can't give money to yourself!")

    db: "Database" = ctx.bot.db
    await db.update(ctx.author.id, "-", amnt)
    await db.check_user(user.id)
    await db.update(user.id, "+", amnt)

    balance = db.get_balance(ctx.author.id)

    embed = Embed(
        color=0xE8BF56,
        title=f"{ctx.author.display_name}'s Transaction",
        description=f"**Amount:** ${amnt}\n\n**Transferred to:** <@{user.id}>",
    )

    embed.set_thumbnail(url=ctx.author.display_avatar)
    embed.set_footer(text=f"Current balance: ${balance}")
    await ctx.reply(embed=embed)


async def setup(bot):
    bot.add_command(give)
