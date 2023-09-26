import io
import asyncio

from discord.ext import commands
from discord import ButtonStyle, File, ui, Interaction

from PIL import Image, ImageDraw, ImageFont

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.words import Words


h, w = (1100, 1300)
PRIMARY = "#111111"
SECONDARY = "#747474"
GREEN = "#508a4d"
YELLOW = "#b2a03c"
GRAY = "#3a3a3c"

FONT = ImageFont.truetype("static/arial.ttf", size=180)

with Image.new(mode="RGBA", size=(h, w), color=PRIMARY) as BASE_PLATE:
    draw = ImageDraw.Draw(BASE_PLATE)

    for y in range(6):
        for x in range(5):
            actX = 75 + (x * 200)
            actY = 75 + (y * 200)

            draw.rectangle(
                ((actX, actY), (100 + (x * 200) + 125, 100 + (y * 200) + 125)),
                outline=SECONDARY,
                width=5,
            )


class MyModal(ui.Modal, title="What is your guess?"):
    guess = ui.TextInput(
        label="Answer",
        max_length=5,
        min_length=5,
    )

    async def on_submit(self, itx: Interaction):
        if len(self.guess.value) > 5:
            return await itx.response.send_message(
                f"<@{itx.user.id}> Your guess must be 5 letters only",
                ephemeral=True,
            )

        await itx.response.defer()  # so it doesn't "error" on discord


class WordleView(ui.View):
    def __init__(
        self,
        *args,
        im: Image.Image,
        user: int,
        word: str,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.im = im
        self.word = word.upper()
        self.user = user
        self.tries = 0

    async def interaction_check(self, itx: Interaction):
        if itx.user.id == self.user:
            return True

        await itx.response.send_message("Not your game.", ephemeral=True)

    @ui.button(label="Guess", style=ButtonStyle.success)
    async def guess(self, itx: Interaction, btn: ui.Button):
        m = MyModal()
        await itx.response.send_modal(m)
        await m.wait()

        guess = m.guess.value.upper()

        # since PIL runs blocking code, we should run it in a different thread
        # so it doesn't block our main asyncio loop.
        board = await asyncio.to_thread(
            self.update_image,
            word=self.word,
            guess=guess,
        )

        self.tries += 1
        if self.tries == 6 or guess == self.word:
            btn.disabled = True
            btn.label = self.word

        await itx.edit_original_response(
            attachments=[board],
            view=self,
        )

    def update_image(self, word: str, guess: str):
        draw = ImageDraw.Draw(im=self.im)

        for x in range(5):
            y = self.tries
            actX = 75 + (x * 200)
            actY = 75 + (y * 200)

            if guess[x] in word:
                if guess[x] == word[x]:
                    fill = GREEN
                else:
                    fill = YELLOW
            else:
                fill = GRAY

            draw.rectangle(
                ((actX, actY), (100 + (x * 200) + 125, 100 + (y * 200) + 125)),
                outline=fill,
                width=5,
                fill=fill,
            )

            draw.text(
                xy=(actX + 15, actY - 23),
                text=guess[x],
                font=FONT,
            )

        buf = io.BytesIO()
        self.im.save(buf, format="PNG")
        buf.seek(0)

        return File(buf, filename="board.png")


@commands.command()
async def wordle(ctx: commands.Context):
    words: "Words" = ctx.bot.words

    word = await words.get_random()

    buf = io.BytesIO()
    image = BASE_PLATE.copy()
    image.save(buf, format="PNG")
    buf.seek(0)

    await ctx.reply(
        file=File(buf, filename="board.png"),
        view=WordleView(
            im=image,
            user=ctx.author.id,
            word=word,
        ),
    )


async def setup(bot: commands.Bot):
    bot.add_command(wordle)