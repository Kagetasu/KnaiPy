import discord
from discord.ext import commands

from utils import Embed


@commands.command()
async def avatar(ctx: commands.Context, user: discord.Member = commands.Author):
    embed = Embed(title=f"{user.name}'s avatar:")
    embed.set_image(url=user.display_avatar)
    await ctx.reply(embed=embed)


async def setup(bot):
    bot.add_command(avatar)
