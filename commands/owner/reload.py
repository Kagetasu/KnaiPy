from discord.ext import commands

from utils import Embed


@commands.command(name="reload")
@commands.is_owner()
async def reload_command(ctx: commands.Context, arg: str):
    try:
        await ctx.bot.reload_extension("commands." + arg)
        await ctx.send(
            embed=Embed(
                color=0x32A852,
                title="Extention Reload",
                description=f"`{arg}` was successfully reloaded",
            )
        )
    except:
        await ctx.send(
            embed=Embed(
                color=0x9C1A36,
                title="Extention Reload",
                description=f"Was unnable to reload `{arg}`",
            )
        )
        raise


async def setup(bot: commands.Bot):
    bot.add_command(reload_command)
