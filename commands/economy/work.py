from discord.ext import commands

from random import choice, uniform
from math import floor

from utils import Embed


jobs = ["Barber", "IT guy", "Plumber", "Dancer", "Pharmacist", "Cashier", "Teacher",
        "Chef", "Electrician", "Mechanic", "Graphic Designer", "Nurse", "Architect", 
        "Lawyer", "Web Developer", "Accountant", "Delivery Driver", "Gardener", 
        "Police Officer", "Firefighter", "Translator", "Journalist", "Fitness Trainer", 
        "Interior Designer", "Real Estate Agent", "Veterinarian", "Astronaut"]



@commands.cooldown(1, 300, commands.BucketType.user)
@commands.command()
async def work(ctx: commands.Context):
    job = choice(jobs)
    amnt = floor(uniform(0.3, 1) * 5000)
    await ctx.bot.db.update(ctx.author.id, "+", amnt)

    balance = await ctx.bot.db.get_balance(ctx.author.id)
    embed = Embed(
        color=0xE8BF56,
        title=f"{ctx.author.display_name}'s Transaction:",
        description=f"**Pay:** ${amnt:,}\n\n**Worked as:** {job}",
    )
    embed.set_thumbnail(url=ctx.author.display_avatar)
    embed.set_footer(text=f"Current balance: ${balance:,}")
    await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    bot.add_command(work)