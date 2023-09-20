import discord
from discord.ext import commands

from databases.economydb import view 

from typing import Annotated

class Embed(discord.Embed):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("color", 0x8662bd)
        super().__init__(*args,**kwargs)

class MoneyConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, arg: str):
        if arg.isdigit():
            if(int(arg) > view(int(ctx.author.id))[0]):
                raise commands.BadArgument(message="You cannot afford this amount")
            
            
            arg = int(arg)
        else:
            arg = arg.lower()
            if(any(s.startswith(arg) for s in ["all", "max", "full"])):
                arg = view(ctx.author.id)[0]
            elif(any(s.startswith(arg) for s in ["half"])):
                arg = view(ctx.author.id)[0] // 2
            else:
                raise commands.BadArgument(message="Invalid amount received")
            
        if(arg <= 0):
            raise commands.BadArgument(message="Amount needs to be greater than zero")
        
        return arg
    
MoneyConverterType = Annotated[int, MoneyConverter]