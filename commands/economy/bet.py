from discord.ext import commands

from random import randint, uniform
from math import floor

from utils import MoneyConverterType, Embed
from config import GREEN, YELLOW, RED

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.economy import Database
    from utils.stats import Stats

@commands.command(aliases=['gamble'])
async def bet(ctx: commands.Context, amnt: MoneyConverterType):
    db: "Database" = ctx.bot.db
    stats: "Stats" = ctx.bot.stats

    player_roll = randint(1,10)
    bot_roll = randint(1,10)

    embed = Embed(title=f"{ctx.author.display_name}'s gamble:")
    embed.set_thumbnail(url=ctx.author.display_avatar)
    embed.add_field(name=f"{ctx.author.display_name}'s roll:", value=f"`{player_roll}`")
    embed.add_field(name=f"Knai's roll:", value=f"`{bot_roll}`")

    if player_roll > bot_roll:
        win_perc = uniform(0.3, 0.7) * 100 // 1
        win_amnt = floor(win_perc * amnt / 100)

        await db.update(ctx.author.id, '+', win_amnt)
        await stats.update_gambling(ctx.author.id, amnt, win_amnt, "win")

        embed.description = f"Congrats! You won **${win_amnt:,}**!\n\n**Percentage won:** {win_perc}%"
        embed.color = GREEN

    elif player_roll < bot_roll:
        await db.update(ctx.author.id, '-', amnt)
        await stats.update_gambling(ctx.author.id, amnt, amnt, 'loss')

        embed.description = "You rolled too low and lost your money :p\n"
        embed.color = RED

    else:
        embed.description = "It's a tie! You keep your money\n"
        embed.color = YELLOW
        
    embed.set_footer(text=f"Current balance: ${await db.get_balance(ctx.author.id)}")
    await ctx.reply(embed=embed)


async def setup(bot):
    bot.add_command(bet)