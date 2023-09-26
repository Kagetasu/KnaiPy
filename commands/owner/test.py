from discord.ext import commands

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.words import Words


@commands.command()
@commands.is_owner()
async def test(ctx: commands.Context):
    db: "Words" = ctx.bot.words

    lst = [i for i in range(10)]
    print(lst)

    
   
async def setup(bot: commands.Bot):
    bot.add_command(test)