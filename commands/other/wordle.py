from discord.ext import commands
from discord import File, ui, ButtonStyle, Interaction
import io
from PIL import Image, ImageDraw, ImageFont

h, w = (1100, 1300)
PRIMARY = "#111111"
SECONDARY = "#747474"
GREEN = "#508a4d"
YELLOW = "#b2a03c"
GRAY = "#3a3a3c"


class MyModal(ui.Modal, title="What is your guess?"):
    answer = ui.TextInput(label="Answer")
    

class MyView(ui.View):
    def __init__(self, *args, ctx: commands.Context, im: Image, word: str,**kwargs):
        self.ctx = ctx
        self.im = im
        self.word = word.upper()
        super().__init__(*args, **kwargs)

    tries = 0

    @ui.button(label="Guess")
    async def guess(self, itx: Interaction, _: ui.Button):

        m = MyModal()
        await itx.response.send_modal(m)
        await m.wait()
        guess = str(m.answer).upper()
        if(len(guess) > 5):
            await itx.followup.send(f"<@{self.ctx.author.id}> Your guess must be 5 letters only")
            return
        
        await itx.followup.send(file=self.update_image(word=self.word, guess=guess), view=self)
        self.tries += 1
        if(self.tries == 5):
            self.stop()

    def update_image(self, word: str, guess: str):
        font = ImageFont.truetype(r"C:\windows\fonts\arial.ttf", size=180)
        draw = ImageDraw.Draw(im=self.im)
        fill: str
        for x in range(5):
            y = self.tries
            actX = 75 + (x * 200)
            actY = 75 + (y * 200)
            if(guess[x] in word):
                if(guess[x] == word[x]):
                    fill = GREEN
                else:
                    fill = YELLOW
            else:
                fill = GRAY
            draw.rectangle([(actX, actY),
                            (100 + (x * 200) + 125, 100 + (y * 200) + 125)],
                            outline=fill, width=5, fill=fill)
            draw.text(xy=(actX+15, actY-23), text=guess[x].upper(), font=font)
        buf = io.BytesIO()
        self.im.save(buf, format="PNG")
        buf.seek(0)
        return File(buf, filename="board.png")
        

@commands.is_owner()
@commands.command()
async def wordle(ctx: commands.Context):
    
    with Image.new(mode="RGBA", size=(h, w), color=PRIMARY) as im:
        draw = ImageDraw.Draw(im)

        for y in range(6):
            for x in range(5):
                actX = 75 + (x * 200)
                actY = 75 + (y * 200)
                draw.rectangle([(actX, actY),
                                (100 + (x * 200) + 125, 100 + (y * 200) + 125)],
                            outline=SECONDARY, width=5)
                font = ImageFont.truetype(r"C:\windows\fonts\arial.ttf", size=180)
                draw.text(xy=(actX+15, actY-23), text="", font=font)

    buf = io.BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    await ctx.reply(file=File(buf, filename="board.png"), view=MyView(ctx=ctx, im=im, word="Crane"))

async def setup(bot: commands.Bot):
    bot.add_command(wordle)