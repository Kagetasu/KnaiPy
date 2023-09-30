from discord.ext import commands

from random import choices, uniform
from math import floor

from utils import Embed, MoneyConverterType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.economy import Database


symbols = ['🍋', '🍋', '🍋', '🍋',
           '🍊', '🍊', '🍊', '🍊',
           '🍉', '🍉', '🍉', '🍉', 
           '🍒', '🍒', '🍒', '🍒',
           '🍇', '🍇', '🍇', '🍇',
           '🍬', '🍬', '🍬', '🍬',
           '🍡', '🍡', '🍡', '🍡',
           'WILD', '2X', '💣']

@commands.command()
async def slots(ctx: commands.Context, amnt:MoneyConverterType):
    db: "Database" = ctx.bot.db
    await db.update(ctx.author.id, "-", amnt)

    symb = choices(symbols, k=3)
    count = 1
    multiplier = 1
   
    if symb[0] == symb[1]:
        count += 1
    if symb[0] == symb[2]:
        count += 1
    if symb[1] == symb[2]:
        count += 1

    for s in symb:
        if s == "WILD":
            count += 1
        elif s == "2X":
            count += 1
            multiplier = 2
        elif s == '💣':
            count = -1
            break

    embed = Embed(
        title=f"{ctx.author.display_name}'s slots game:",
        description=f"**{symb[0]}** | **{symb[1]}** | **{symb[2]}**\n\n"
        )
    
    if count > 1:
        win = floor(uniform(0.3, 0.7)*amnt)
        if count == 2:
            win = win * multiplier
            embed.description += f"Congrats! You won **${win:,}!!**"
            embed.color = 0x32A852
        else:
            win = win * 4
            embed.description += f"**JACKPOT!!!** You won **${win:,}!!**"
            embed.color = 0xE8BF56

        await db.update(ctx.author.id, '+', amnt=win+amnt)
    else:  
        if(count == -1):
            embed.description += "You got **BOMBED!** R.I.P 💀"
            embed.color = 0x3B020A
        else:
            embed.description += "  You lost..."
            embed.color = 0x9C1A36


    balance = await db.get_balance(ctx.author.id)
    embed.set_footer(text=f"Current balance: ${balance:,}")
    await ctx.reply(embed = embed)

    


async def setup(bot):
    bot.add_command(slots)