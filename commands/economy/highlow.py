from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle, Interaction

from utils import Embed

from random import randrange, choice

from databases.economydb import update



class hlView(View):
    def __init__(self, *args, ctx: commands.Context, result: str,num: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.result = result
        self.num = num

        high = Button(
            style=ButtonStyle.secondary,
            emoji='⬆️',
            custom_id='h',
                      )
        low = Button(
            style=ButtonStyle.secondary,
            emoji='⬇️',
            custom_id='l'
        )

        high.callback = self.generic_callback(high)
        low.callback = self.generic_callback(low)

        self.add_item(high)
        self.add_item(low)
    
    def generic_callback(self, button: Button):
        async def callback(itx: Interaction):

            for b in self.children:
                b.disabled = True
                if(b.custom_id != self.result):
                    b.style = ButtonStyle.red
                else:
                    b.style = ButtonStyle.green

            embed = itx.message.embeds[0]

            if(button.custom_id == self.result):
                win = randrange(1500, 3001)
                embed.color=0x32a852
                embed.description = f"Correct! You won **${win}**!"
                update(self.ctx.author.id, '+', win)
            else:
                embed.color=0x9c1a36
                embed.description = f"Incorrect!"

            embed.description +=  f"\n\nThe number was `{self.num}`"
            await itx.response.edit_message(embed=embed, view=self)
        return callback
        




@commands.command(aliases= ['hl'])
async def highlow(ctx: commands.Context):
    
    num = randrange(5,100)
    rng = list(range(2, 101))
    rng.remove(num)
    hint = choice(rng)
    result = ''
    if(num > hint):
        result = 'h'
    else:
        result = 'l'
    embed = Embed(
        title=f"{ctx.author.display_name}'s HighLow game:",
        description=f"Your hint is `{hint}`. Is the number higher or lower?"
    )
    await ctx.reply(embed=embed,view=hlView(ctx=ctx, result=result, num=num))
    


async def setup(bot):
    bot.add_command(highlow)