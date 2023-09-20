from typing import Literal
from discord import ui, ButtonStyle
import discord
from discord.ext import commands

from utils import Embed

from random import randrange, choice


class HighLowView(ui.View):
    def __init__(
        self,
        *args,
        ctx: commands.Context,
        result: Literal["high", "low"],
        num: int,
        embed: Embed,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.result = result
        self.num = num
        self.embed = embed

    def disable_buttons(self) -> None:
        for child in self.children:
            if isinstance(child, ui.Button):
                if child.emoji == self.result:
                    child.style = ButtonStyle.green
                else:
                    child.style = ButtonStyle.red

                child.disabled = True

    async def logic(
        self,
        itx: discord.Interaction,
        answer: Literal["high", "low"],
    ) -> None:
        embed = self.embed  # alias

        if answer == self.result:
            win = randrange(1500, 3001)
            embed.color = 0x32A852
            embed.description = f"Correct! You won **${win}**!"
            await self.ctx.bot.db.update(self.ctx.author.id, "+", win)
        else:
            embed.color = 0x9C1A36
            embed.description = f"Incorrect!"

        embed.description += f"\n\nThe number was `{self.num}`"
        await itx.response.edit_message(embed=embed, view=self)

    @ui.button(emoji="⬆️", style=ButtonStyle.secondary)
    async def high(self, itx: discord.Interaction, _: ui.Button):
        await self.logic(itx, "high")

    @ui.button(emoji="⬇️", style=ButtonStyle.secondary)
    async def low(self, itx: discord.Interaction, _: ui.Button):
        await self.logic(itx, "low")


@commands.command(aliases=["hl"])
async def highlow(ctx: commands.Context):
    num = randrange(5, 100)
    rng = list(range(2, 101))
    rng.remove(num)
    hint = choice(rng)

    if num > hint:
        result = "high"
    else:
        result = "low"

    embed = Embed(
        title=f"{ctx.author.display_name}'s HighLow game:",
        description=f"Your hint is `{hint}`. Is the number higher or lower?",
    )

    await ctx.reply(
        embed=embed,
        view=HighLowView(
            ctx=ctx,
            result=result,
            num=num,
            embed=embed,
        ),
    )


async def setup(bot):
    bot.add_command(highlow)
