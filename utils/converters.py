import discord
from discord.ext import commands

from typing import Annotated


class MoneyConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, arg: str):
        db = ctx.bot.db
        balance = await db.get_balance(ctx.author.id)

        if arg.isdigit():
            amount = int(arg)
            if amount > balance:
                raise commands.BadArgument(message=f"You cannot afford this amount as you only have **${balance}**")
        else:
            arg = arg.lower()
            if any(s.startswith(arg) for s in ("all", "max", "full",)):
                amount = balance
            elif any(s.startswith(arg) for s in ("half",)):
                amount = balance // 2
            else:
                print(arg)
                raise commands.BadArgument(message="Invalid amount received")
        
        if amount <= 0:
            raise commands.BadArgument(message="Amount needs to be greater than zero")
        
        return amount
    
MoneyConverterType = Annotated[int, MoneyConverter]
