from discord.ext import commands
from databases.economydb import view, update
from discord import Embed

from random import choice, uniform
from math import floor


jobs = ["Barber", "IT guy", "Plumber", "Dancer", "Pharmacist", "Cashier", "Teacher"]

@commands.cooldown(1, 300, commands.BucketType.user)
@commands.command()
async def work(ctx: commands.Context):
    
    job = choice(jobs)
    amnt = floor(uniform(0.3, 1)*5000)
    update(ctx.author.id, '+', amnt)

    embed = Embed(
        color=0xe8bf56,
        title=f"{ctx.author.display_name}'s Transaction:",
        description=f"**Pay:** ${amnt}\n\n**Worked as:** {job}")
    embed.set_thumbnail(url=ctx.author.display_avatar)
    embed.set_footer(text=f"Current balance: ${view(ctx.author.id)[0]}")
    await ctx.reply(embed=embed)
    
async def setup(bot: commands.Bot):
    bot.add_command(work)