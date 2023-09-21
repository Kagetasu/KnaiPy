import discord
from discord.ext import commands

from typing import Union

from utils import Embed


@commands.command()
async def avatar(
    ctx: commands.Context,
    user: Union[discord.Member, discord.User] = commands.Author,
):
    embed = Embed(title=f"{user.name}'s avatar:")
    embed.set_image(url=user.display_avatar)
    await ctx.reply(embed=embed)


async def setup(bot):
    bot.add_command(avatar)
