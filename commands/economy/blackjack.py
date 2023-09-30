from discord import ui, Interaction, ButtonStyle, Message

from discord.ext import commands

from random import shuffle, uniform

from utils import Embed, MoneyConverterType
from config import GREEN, RED, YELLOW

from typing import Optional, TypedDict, TYPE_CHECKING

from enum import Enum, auto

if TYPE_CHECKING:
    from utils.economy import Database

SUITS = ['♠️', '♦️', '♣️', '♥️']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'K', 'Q', 'A']


class GameStatus(Enum):
    Win = auto()
    Tie = auto()
    Loss = auto()
    Continue = auto()

    message = None

    def with_message(self, content: str):
        self.message = content
        return self

def check_hand(
        p: int,
        d: int,
        stand: bool = False
) -> GameStatus:
    result = GameStatus.Continue

    if p == 21:
        result = GameStatus.Win.with_message("You got **BLACKJACK**!! You won **?%** of your bet!")


    if d == 21:
        result = GameStatus.Loss.with_message("Dealer hit **BLACKJACK**!! You lost your money :<")
        if p == 21:
            result = GameStatus.Tie.with_message("You both tied with **21**!")

 
    if d > 21:
        result = GameStatus.Win.with_message("Dealer **BUSTED**!! You won **?%** of your bet!")


    if p > 21:
        result = GameStatus.Loss.with_message("You **BUSTED**!!")
        if d > 21:
            result = GameStatus.Tie.with_message("You both **BUSTED**!! It's a tie")    
    

    if stand and result == GameStatus.Continue:
        if p > d:
            result = GameStatus.Win.with_message("You have more than the dealer!! You win **?%** of your bet!")
        elif p == d:
            result = GameStatus.Tie.with_message(f"You both tied with **{p}**!")
        else:
            result = GameStatus.Loss.with_message("Dealer has more than you!! You lost :<")
    
    return result


class Holder(TypedDict):
    name: str
    user_id: int
    avatar_url: str


class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

        if rank in ("J", "K", "Q"):
            self.value = 10
        elif rank == "A":
            self.value = 11
        else:
            self.value = int(self.rank)

    def __str__(self):
        return f"`{self.suit}{self.rank}`"
    


class Deck:
    def __init__(
            self,
            *,
            holder: Optional[Holder] = None,
            main_deck: list[Card]
    ):
        self.main_deck = main_deck
        self.cards: list[Card] = []

        self.aces = 0
        self.value = 0

        self.holder = holder or {
            "name": "Knai",
            "user_id": 0,
            "avatar_url": "...",
        }
    
    def __str__(self):
        return " ".join([f"{card}" for card in self.cards])


    def draw(self, times: int = 1):
        for _ in range(times):
            card = self.main_deck.pop()
            self.value += card.value

            if card.rank == "A":
                self.aces += 1

            if self.value > 21 and self.aces:
                self.value -= 10
                self.aces -= 1

            self.cards.append(card)



class BlackJackView(ui.View):
    def __init__(
            self,
            *args,
            main_deck: list[Card],
            player_deck: Deck,
            amnt: int,
            db: "Database",
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.main_dec = main_deck
        self.amnt = amnt
        self.player_deck = player_deck
        self.db = db
        self.message: Optional[Message] = None

        self.opponent_deck = Deck(main_deck=main_deck)

        self.player_deck.draw(2)
        self.opponent_deck.draw(2)


    def create_embed(
            self,
            *,
            footer: Optional[str] = None,
            reveal_deck: bool = False,
            **kwargs,
    ):
        embed = Embed(**kwargs)
        embed.title = f"{self.player_deck.holder['name']}'s BlackJack"
        embed.set_thumbnail(url=self.player_deck.holder["avatar_url"])
        embed.set_footer(text=footer)

        embed.add_field(
            name=f"{self.player_deck.holder['name']}'s deck:",
            value=f"Cards - {self.player_deck}\nTotal - `{self.player_deck.value}`",
        )

        if reveal_deck:
            embed.add_field(
                name=f"{self.opponent_deck.holder['name']}'s deck:",
                value=f"Cards - {self.opponent_deck}\nTotal - `{self.opponent_deck.value}`",
            )
        else:
            embed.add_field(
                name=f"{self.opponent_deck.holder['name']}'s deck:",
                value=f"Cards - {self.opponent_deck.cards[0]} `?`\n Total - `?`",
            )


        return embed
    
    async def interaction_check(self, itx: Interaction) -> bool:
        if self.player_deck.holder['user_id'] == itx.user.id:
            return True
        return False
    
    async def on_timeout(self) -> None:
        for child in self.children:
            if isinstance(child, ui.Button):
                child.disabled = True
        
        if self.message:
            embed = self.create_embed(color = 0x9C1A36, description = "Game timed out.")
            await self.message.edit(embed=embed, view=self)
        
    @ui.button(label="HIT", style=ButtonStyle.secondary)
    async def hit(self, itx: Interaction, _: ui.Button["BlackJackView"]):
        self.player_deck.draw()

        winperc = uniform(0.4, 0.9) * 100 // 1
        win_amnt = self.amnt + winperc * self.amnt // 100

        result = check_hand(self.player_deck.value, self.opponent_deck.value)

        if result == GameStatus.Continue:
            await itx.response.edit_message(embed=self.create_embed(), view=self)
        
        else:
            embed = self.create_embed(reveal_deck=True)
            

            if result == GameStatus.Win:
                embed.color = GREEN

                await self.db.update(itx.user.id, "+", win_amnt)
                
            else:
                embed.color = RED

            embed.description = result.message.replace("?", str(winperc))
            embed.set_footer(text=f"Current balance: ${await self.db.get_balance(itx.user.id):,}")
            await itx.response.edit_message(embed=embed, view=None)
            

            


    @ui.button(label="STAND", style=ButtonStyle.secondary)
    async def stand(self, itx: Interaction, _: ui.Button["BlackJackView"]):
        winperc = uniform(0.4, 0.9) * 100 // 1
        win_amnt = self.amnt + winperc * self.amnt // 100
        
        while self.opponent_deck.value < 17:
            self.opponent_deck.draw()
        
        result = check_hand(self.player_deck.value, self.opponent_deck.value, stand=True)

        embed = self.create_embed(reveal_deck=True)

        if result == GameStatus.Tie:
            await self.db.update(itx.user.id, "+", self.amnt)
            embed.color = YELLOW

        elif result == GameStatus.Loss:
            embed.color = RED

        else:
            embed.color = GREEN

            await self.db.update(itx.user.id, "+", win_amnt)
        
        embed.description = result.message.replace("?", str(winperc))
        embed.set_footer(text=f"Current balance: ${await self.db.get_balance(itx.user.id):,}")
        await itx.response.edit_message(embed=embed, view=None)

        



@commands.command(aliases = ['bj'])
async def blackjack(
    ctx: commands.Context,
    amnt: MoneyConverterType
):
    db: "Database" = ctx.bot.db

    await db.update(ctx.author.id, "-", amnt) # Locking the amount

    main_deck = []

    for suit in SUITS:
        for rank in RANKS:
            main_deck.append(Card(suit=suit, rank=rank))
    
    shuffle(main_deck)

    view = BlackJackView(
        main_deck=main_deck,
        player_deck=Deck(
            main_deck=main_deck,
            holder={
                "name": ctx.author.display_name,
                "user_id": ctx.author.id,
                "avatar_url": ctx.author.display_avatar.url,
            }
        ),
        amnt=amnt,
        db=db
    )

    embed = view.create_embed(
        reveal_deck=False,
    )

    result = check_hand(view.player_deck.value, view.opponent_deck.value)
    
    if result is not GameStatus.Continue:
        winperc = uniform(0.4, 0.9) * 100 // 1
        win_amnt = amnt + winperc * amnt // 100
        embed = view.create_embed(
            reveal_deck=True
        )
        if result == GameStatus.Tie:
                await db.update(ctx.author.id, "+", amnt)
                embed.color = YELLOW

        elif result == GameStatus.Loss:
            embed.color = RED

        else:
            embed.color = GREEN
            await db.update(ctx.author.id, "+", win_amnt)
        
        embed.description = result.message.replace("?", str(winperc))
        embed.set_footer(text=f"Current balance: ${await db.get_balance(ctx.author.id):,}")

        view.stop()
        await ctx.reply(embed=embed, view=None)
        
    else:
        view.message = await ctx.reply(
            embed=embed,
            view=view
        )

    

async def setup(bot: commands.Bot):
    bot.add_command(blackjack)