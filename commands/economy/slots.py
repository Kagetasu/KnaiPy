from discord.ext import commands
from discord import Embed

from typing import Annotated

from random import choices, uniform
from math import floor

from databases.economydb import update, view, lock, unlock

from utils import MoneyConverter

symbols = ['🍋', '🍋', '🍋', '🍋',
           '🍊', '🍊', '🍊', '🍊',
           '🍉', '🍉', '🍉', '🍉', 
           '🍒', '🍒', '🍒', '🍒',
           '🍇', '🍇', '🍇', '🍇',
           '🍬', '🍬', '🍬', '🍬',
           '🍡', '🍡', '🍡', '🍡',
           'WILD', '2X', '💣']

@commands.command()
async def slots(ctx: commands.Context, amnt:Annotated[int, MoneyConverter]):

    lock(ctx.author.id, amnt)

    symb = choices(symbols, k=3)
    count = 1
    multiplier = 1
   
    if(symb[0] == symb[1]):
        count += 1
    if(symb[0] == symb[2]):
        count += 1
    if(symb[1] == symb[2]):
        count += 1

    for s in symb:
        if(s == 'WILD'):
            count += 1
        elif(s == '2X'):
            count += 1
            multiplier = 2
        elif(s == '💣'):
            count = -1
            break

    embed = Embed(title=f"{ctx.author.display_name}'s slots game:", description=f"**{symb[0]}** | **{symb[1]}** | **{symb[2]}**\n\n")
    
    if(count > 1):
        win = floor(uniform(0.3, 0.7)*amnt)
        if(count == 2):
            win = win * multiplier
            embed.description += f"Congrats! You won **${win}!!**"
            embed.color = 0x32a852
        else:
            win = win * 4
            embed.description += f"**JACKPOT!!!** You won **${win}!!**"
            embed.color = 0xe8bf56

        update(ctx.author.id, '+', amnt=win)
    else:  
        if(count == -1):
            embed.description += "You got **BOMBED!** R.I.P 💀"
            embed.color = 0x3b020a
        else:
            embed.description += "  You lost..."
            embed.color = 0x9c1a36

        update(ctx.author.id, '-', amnt=amnt)

    unlock(ctx.author.id, amnt)
    
    embed.set_footer(text=f"Current balance: ${view(ctx.author.id)[0]}")
    
    await ctx.reply(embed = embed)

    


async def setup(bot):
    bot.add_command(slots)