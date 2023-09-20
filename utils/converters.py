import discord
from discord.ext import commands

from typing import Annotated


class MoneyConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, arg: str):
        db = ctx.bot.db  # just an alias to save time

        if arg.isdigit():
            amount = int(arg)
            if amount > (await db.view_user(ctx.author.id))[0]:
                raise commands.BadArgument(message="You cannot afford this amount")
        else:
            arg = arg.lower()
            if any(s.startswith(arg) for s in ["all", "max", "full"]):
                amount = (await db.view_user(ctx.author.id))[0]
            elif any(s.startswith(arg) for s in ["half"]):
                amount = (await db.view_user(ctx.author.id))[0] // 2
            else:
                raise commands.BadArgument(message="Invalid amount received")

        if amount <= 0:
            raise commands.BadArgument(message="Amount needs to be greater than zero")

        return amount


MoneyConverterType = Annotated[int, MoneyConverter]
