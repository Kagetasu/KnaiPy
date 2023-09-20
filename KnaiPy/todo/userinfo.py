from discord.ext import commands
from discord import Embed

@commands.command()
async def userinfo(ctx: commands.Context, id = None):
    return
    if(ctx.message.mentions):
        id = ctx.message.mentions[0].id
    if(id == None):
        id = ctx.author.id

    member = ctx.guild.get_member(id)
    roles = [f"<@&{role.id}>" for role in member.roles if role.name != "@everyone"]
    print(member._permissions)
    return
    if(member == None):
        await ctx.reply("No member found")
        return
    
    embed = Embed()
    embed.set_author(name=member.name.capitalize(), icon_url=member.display_avatar)
    embed.set_thumbnail(url=member.display_avatar)
    embed.add_field(name="Joined at:", value=member.joined_at.date(), inline=True)
    embed.add_field(name="Registered at:", value=member.created_at.date(), inline=True)
    embed.add_field(name="Roles", value=', '.join(roles), inline=False)
    embed.add_field(name="Permissions:", value=', '.join(member.guild_permissions))
    await ctx.reply(embed=embed)

async def setup(bot):
    bot.add_command(userinfo)