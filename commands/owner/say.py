from discord.ext import commands

@commands.is_owner()
@commands.command()
async def say(ctx: commands.Context, *, args):
    await ctx.message.delete(delay=0)
    await ctx.send(args)
    


async def setup(bot):
    bot.add_command(say)