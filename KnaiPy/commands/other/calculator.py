from discord.ext import commands
from discord import ui, Embed, ButtonStyle, Interaction



buttons = [
    ["(", ")", "C", "/"],
    ["7", "8", "9", "x"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["ESC", "0", ".", "="]
]

equation = " "
embed = Embed(title="Calculator", description=f"```{equation}```", color=0x8662bd)

class Calculator(ui.View):
    def __init__(self, *args, ctx:commands.Context, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx

        for i, row in enumerate(buttons):
            for e in row:
                b = ui.Button(
                    label=e,
                    row=i
                )
                if("0" <= e <= "9") or (e == "."):
                    b.style = ButtonStyle.blurple
                    b.callback = self.generic_callback(b)
                elif(e == "="):
                    b.style = ButtonStyle.green
                    b.callback = self.eq_callback
                elif(e == "ESC"):
                    b.style = ButtonStyle.red
                    b.callback = self.esc_callback
                elif(e == "C"):
                    b.callback = self.c_callback
                else:
                    b.callback = self.generic_callback(b)
                self.add_item(b)

    def generic_callback(self, btn: ui.Button):
        async def actual_callback(interaction: Interaction):
            global equation
            equation += btn.label
            embed.description = f"```{equation}```"
            await interaction.response.edit_message(embed=embed)
        return actual_callback
        
    async def c_callback(self, interaction: Interaction):
        global equation
        equation = " "
        embed.description = f"```{equation}```"
        await interaction.response.edit_message(embed=embed, view=self)
        
    async def esc_callback(self, interaction: Interaction):
        embed.description = "```Cancelled...```"
        await interaction.response.edit_message(embed=embed, view=None)

    async def eq_callback(self, interaction: Interaction):
        try:
            embed.description = f"```{eval(equation)}```"
            embed.color = 0x32a852
        except:
            embed.description = f"```Invalid syntax...```"
            embed.color = 0x9c1a36
        await interaction.response.edit_message(embed=embed, view=None)

    async def interaction_check(self, interaction: Interaction):
        if(interaction.user == self.ctx.author):
            return True
        else:
            return False

    

@commands.command(aliases = ['calc'])
async def calculator(ctx):
    await ctx.send(embed=embed, view=Calculator(ctx=ctx))

async def setup(bot):
    bot.add_command(calculator)