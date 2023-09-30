import discord
from discord.ext import commands

from utils import Embed

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from utils.economy import Database


@commands.command(aliases = ['bal'])
async def balance(
    ctx: commands.Context,
    user: Union[discord.Member, discord.User] = commands.Author
):
    db : "Database"  = ctx.bot.db
    
    bal = await db.get_balance(user.id)

    embed = Embed(title=user.display_name)
    embed.set_thumbnail(url=user.display_avatar)
    embed.description = f"**Balance:** ${bal:,}"
    
    await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(balance)