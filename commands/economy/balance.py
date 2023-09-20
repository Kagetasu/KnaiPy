import discord
from discord.ext import commands

from utils import Embed

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.economy import Database


@commands.command(aliases=["bal"])
async def balance(ctx: commands.Context, user: discord.User = commands.Author):
    db: "Database" = ctx.bot.db

    bal = (await db.view_user(user.id))[0]

    embed = Embed(title=user.display_name)
    embed.set_thumbnail(url=user.display_avatar)
    embed.description = f"**Balance:** ${bal}"
    await ctx.reply(embed=embed)


async def setup(bot):
    bot.add_command(balance)
