from discord.ext import commands
from discord import ui, ButtonStyle, Interaction

from utils import Embed

buttons = [
    ["(", ")", "C", "/"],
    ["7", "8", "9", "x"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["ESC", "0", ".", "="],
]


class Calculator(ui.View):
    def __init__(self, *args, ctx: commands.Context, embed: Embed, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx

        self.equation = " "
        self.embed = embed

        for i, row in enumerate(buttons):
            for e in row:
                b = ui.Button(label=e, row=i)
                if ("0" <= e <= "9") or (e == "."):
                    b.style = ButtonStyle.blurple
                    b.callback = self.generic_callback(b)
                elif e == "=":
                    b.style = ButtonStyle.green
                    b.callback = self.eq_callback
                elif e == "ESC":
                    b.style = ButtonStyle.red
                    b.callback = self.esc_callback
                elif e == "C":
                    b.callback = self.c_callback
                else:
                    b.callback = self.generic_callback(b)
                self.add_item(b)

    def generic_callback(self, btn: ui.Button):
        async def actual_callback(interaction: Interaction):
            self.equation += btn.label  # type: ignore
            self.embed.description = f"```\n{self.equation}```"
            await interaction.response.edit_message(embed=self.embed)

        return actual_callback

    async def c_callback(self, interaction: Interaction):
        self.equation = " "
        self.embed.description = f"```\n{self.equation}```"
        await interaction.response.edit_message(embed=self.embed, view=self)

    async def esc_callback(self, interaction: Interaction):
        self.embed.description = "```\nCancelled...```"
        await interaction.response.edit_message(embed=self.embed, view=None)

    async def eq_callback(self, interaction: Interaction):
        try:
            self.embed.description = f"```\n{eval(self.equation)}```"
            self.embed.color = 0x32A852
        except:
            self.embed.description = f"```Invalid syntax...```"
            self.embed.color = 0x9C1A36
        await interaction.response.edit_message(embed=self.embed, view=None)

    async def interaction_check(self, interaction: Interaction):
        if interaction.user == self.ctx.author:
            return True

        await interaction.response.send_message("Not your calculator!", ephemeral=True)


@commands.command(aliases=["calc"])
async def calculator(ctx):
    embed = Embed(
        title="Calculator",
        description=f"```\n```",
        color=0x8662BD,
    )

    await ctx.send(
        embed=embed,
        view=Calculator(ctx=ctx, embed=embed),
    )


async def setup(bot):
    bot.add_command(calculator)
