from discord.ext import commands
from discord import ui, ButtonStyle, Message, Interaction, User

from utils import Embed, MoneyConverterType

from random import shuffle

from config import RED, GREEN, YELLOW

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.economy import Database


class ScratchView(ui.View):
    def __init__(
            self,
            *args,
            user: User,
            message: Message,
            rewards: list[dict],
            amnt: int,
            db: "Database",
            **kwargs
    ):
        self.user = user
        self.message = message
        self.rewards = rewards
        self.amnt = amnt
        self.db = db

        self.multi = 0.0
        self.tries = 5
        self.scratched = []

        super().__init__(*args, **kwargs)

        for row in range(5):
            for col in range(5):
                b = ui.Button(label="\u2800", style=ButtonStyle.gray, row=row)
                b.callback = self.generic_callback(b)
                self.add_item(b)

    def generic_callback(self, btn: ui.Button):
        async def callback(itx: Interaction):
            
            self.tries -= 1
            
            reward = self.rewards.pop()
            self.multi += reward["multi"]
            btn.label = reward["label"]

            if(btn.label == "\u2800"):
                btn.style = ButtonStyle.red
            else:
                self.scratched.append(reward["label"])
                btn.style = ButtonStyle.green

            btn.disabled = True

            embed = self.create_embed()

            if(self.tries == 0):

                for child in self.children:
                    if isinstance(child, ui.Button):
                        child.disabled = True
                        if child.style == ButtonStyle.gray:
                            reward = self.rewards.pop()
                            child.label = reward["label"]

                win = int(self.multi * self.amnt // 1)
                await self.db.update(self.user.id, "+", win)
            
                embed.set_footer(text=f"Current balance: ${await self.db.get_balance(self.user.id):,}")

                if win < self.amnt:
                    embed.color = RED
                    embed.description += f"\n\nYou were only able to get **${win:,}** back :<"
                elif win > self.amnt:
                    embed.color = GREEN
                    embed.description += f"\n\nYou won **${win:,}**!"
                else:
                    embed.color = YELLOW
                    embed.description += f"\n\nWell you were able to get your money back, nothing more :p"



            await itx.response.edit_message(embed=embed, view=self)

        return callback
    
    def create_embed(self):
        user = self.user

        embed = Embed()
        embed.title = f"{user.display_name}'s scratch game:"
        embed.set_thumbnail(url=user.display_avatar)
        embed.description = f"You have **{self.tries}** scratches left\n\n"
        if len(self.scratched):
            embed.description += f"**Rewards claimed:**\n• " + '\n• '.join(self.scratched) + f"\n\n**Total multiplier**: x{round(self.multi * 100) / 100}"

        return embed
        

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id == self.user.id:
            return True
        else:
            await interaction.response.send_message("Not your game", ephemeral=True)

@commands.command()
async def scratch(ctx: commands.Context, amnt: MoneyConverterType):
    db: "Database" = ctx.bot.db

    await db.update(ctx.author.id, "-", amnt)

    rewards = (
    [{"id": "bag", "label": "💰", "multi": 0.15}] * 9 +
    [{"id": "medal", "label": "🏅", "multi": 0.5}] * 3 +
    [{"id": "trophy", "label": "🏆", "multi": 0.75}] * 2 +
    [{"id": "crown", "label": "👑", "multi": 1.5}] * 1 +
    [{"id": "empty", "label": "\u2800", "multi": 0}] * 10
    )
    shuffle(rewards)

    view = ScratchView(user=ctx.author, message=ctx.message, rewards=rewards, amnt=amnt, db=db)

    await ctx.reply(embed=view.create_embed(), view=view)

async def setup(bot: commands.Bot):
    bot.add_command(scratch)