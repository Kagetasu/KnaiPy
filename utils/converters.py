import discord
from discord.ext import commands

from typing import Annotated


class MoneyConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, arg: str):
        db = ctx.bot.db  # just an alias to save time
        balance = await db.get_balance(ctx.author.id)

        if arg.isdigit():
            amount = int(arg)
            if amount > balance:
                raise commands.BadArgument(
                    f"You cannot afford this amount, you can only afford ${balance}"
                )
        else:
            arg = arg.lower()
            if any(s.startswith(arg) for s in ["all", "max", "full"]):
                amount = balance
            elif any(s.startswith(arg) for s in ["half"]):
                amount = balance // 2
            else:
                raise commands.BadArgument("Invalid amount received")

        if amount <= 0:
            raise commands.BadArgument("Amount needs to be greater than zero")

        return amount


MoneyConverterType = Annotated[int, MoneyConverter]
