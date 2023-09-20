from discord.ext import commands
from databases.economydb import view
from discord import Embed, User

@commands.command(aliases = ['bal'])
async def balance(ctx: commands.Context, user: User = commands.Author):
    bal = view(user.id)[0]
    embed = Embed(color=0x8662bd, title=user.display_name)
    embed.set_thumbnail(url=user.display_avatar)
    
    embed.description = f"**Balance:** ${bal}"
    await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(balance)