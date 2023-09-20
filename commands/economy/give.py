from discord.ext import commands
from discord import Embed, User

from databases.economydb import view, update

from utils import MoneyConverter

from typing import Annotated

@commands.command()
async def give(ctx: commands.Context, user: User, amnt:Annotated[int, MoneyConverter]):

    if(user.id == ctx.author.id):
        await ctx.reply(f"Transferred **${amnt}** from <@{user.id}> to <@{user.id}>")
        return
        
    embed = Embed(
        color=0xe8bf56,
        title=f"{ctx.author.display_name}'s Transaction",
        description=f"**Amount:** ${amnt}\n\n**Transferred to:** <@{user.id}>"
        )
    
    embed.set_thumbnail(url=ctx.author.display_avatar)
    update(ctx.author.id, '-', amnt)
    update(user.id, '+', amnt)
    embed.set_footer(text=f"Current balance: ${view(ctx.author.id)[0]}")
    await ctx.reply(embed=embed)
    

async def setup(bot):
    bot.add_command(give)