from discord.ext import commands
from random import random, uniform
from math import floor
from databases.economydb import update, view

@commands.command()
async def bet(ctx: commands.Context, amnt: int):

    bal = view(ctx.author.id)[0]

    if(amnt > bal):
        await ctx.reply("You do not have that much money")
        return
    
    if(random() >= 0.55):
        win = floor(uniform(0.3, 0.5) * amnt)
        await ctx.send(f"Congrats! You won **${win}**!")
        update(ctx.author.id, '+', win)
    else:
        await ctx.send("You lost 😝")
        update(ctx.author.id, '-', amnt)



async def setup(bot):
    bot.add_command(bet)