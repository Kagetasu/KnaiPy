from discord.ext import commands
from discord import Embed

@commands.command()
async def avatar(ctx: commands.Context, id: int=None):
    if(ctx.message.mentions):
        id = ctx.message.mentions[0].id
    if(id == None):
        id = ctx.author.id
    member = ctx.guild.get_member(id)
    if(member == None):
        await ctx.reply("No member found")
        return
    embed = Embed(title=f"{member.name.title()}'s avatar:")
    embed.set_image(url=member.display_avatar)
    await ctx.reply(embed=embed)


async def setup(bot):
    bot.add_command(avatar)