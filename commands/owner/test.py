from discord.ext import commands


@commands.command()
async def test(ctx: commands.Context):
    knai: commands.bot.Bot = ctx.bot
    print(ctx.bot.help_command)


async def setup(bot: commands.Bot):
    bot.add_command(test)
