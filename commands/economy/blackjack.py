from discord import ui, Interaction, ButtonStyle, Message
from discord.ext import commands

from random import choice, uniform

from utils import Embed, MoneyConverterType

from typing import Optional, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from utils.economy import Database

SUITS = ["♠️", "♦️", "♣️", "♥️"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]


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
        main_deck: list[Card],
    ):
        self.main_deck = main_deck
        self.cards: list[Card] = []
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
            card = choice(self.main_deck)

            if (card.rank == "A") and (card.value + self.value > 21):
                self.value += 1
            else:
                self.value += card.value

            self.cards.append(card)
            self.main_deck.remove(card)


class BlackJackView(ui.View):
    def __init__(
        self,
        *args,
        main_deck: list[Card],
        player_deck: Deck,
        amnt: int,
        db: "Database",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.main_deck = main_deck
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
            name=f"{self.player_deck.holder['name']}'s deck:'",
            value=f"Cards - {self.player_deck}\nTotal - `{self.player_deck.value}`",
        )

        if reveal_deck:
            embed.add_field(
                name=f"{self.opponent_deck.holder['name']}'s deck",
                value=f"Cards - {self.opponent_deck}\nTotal - `{self.opponent_deck.value}`",
            )
        else:
            embed.add_field(
                name=f"{self.opponent_deck.holder['name']}'s deck",
                value=f"Cards - {self.opponent_deck.cards[0]} `?`\n Total - `?`",
            )

        return embed

    async def interaction_check(self, itx: Interaction) -> bool:
        if self.player_deck.holder["user_id"] == itx.user.id:
            return True
        return False

    async def on_timeout(self) -> None:
        for child in self.children:
            if isinstance(child, ui.Button):
                child.disabled = True

        if self.message:
            embed = self.create_embed(color=0x9C1A36, description="Game timed out.")
            await self.message.edit(embed=embed, view=self)

    @ui.button(label="HIT", style=ButtonStyle.secondary)
    async def hit(self, itx: Interaction, _: ui.Button["BlackJackView"]):
        self.player_deck.draw()
        if self.player_deck.value > 21:
            await self.db.update(itx.user.id, "-", self.amnt)

            balance = await self.db.get_balance(itx.user.id)

            embed = self.create_embed(
                description="You **Busted**!",
                color=0x9C1A36,
                footer=f"Current balance: ${balance}",
                reveal_deck=True,
            )
            await itx.response.edit_message(
                embed=embed,
                view=None,
            )
            self.stop()

        elif self.player_deck.value == 21:
            if self.opponent_deck.value == 21:
                await self.db.update(itx.user.id, "-", self.amnt)

                balance = await self.db.get_balance(itx.user.id)

                embed = self.create_embed(
                    color=0x9C1A36,
                    description="Busted! Dealer has blackjack.",
                    footer=f"Current balance: ${balance}",
                )
            else:
                winperc = uniform(0.4, 0.9) * 100 // 1

                await self.db.update(itx.user.id, "+", winperc * self.amnt // 100)
                balance = await self.db.get_balance(itx.user.id)

                embed = self.create_embed(
                    color=0x32A852,
                    description="Congrats! You won **{winperc}%** of your bet.",
                    footer=f"Current balance: ${balance}",
                )

            await itx.response.edit_message(embed=embed, view=None)

        else:
            await itx.response.edit_message(
                embed=self.create_embed(),
            )

    @ui.button(label="STAND", style=ButtonStyle.secondary)
    async def stand(self, itx: Interaction, _: ui.Button["BlackJackView"]):
        self.opponent_deck.draw()

        winperc = uniform(0.4, 0.9) * 100 // 1
        if self.opponent_deck.value > 21:
            await self.db.update(itx.user.id, "+", winperc * self.amnt // 100)

            embed = self.create_embed(
                color=0x9C1A36,
                description="Dealer busted. You won **{winperc}%** of your bet.",
                reveal_deck=True,
            )

        if self.player_deck.value > self.opponent_deck.value:
            await self.db.update(itx.user.id, "+", winperc * self.amnt // 100)

            embed = self.create_embed(
                color=0x32A852,
                description=f"You have more than the dealer! You won **{winperc}%** of your bet!",
                reveal_deck=True,
            )
        elif self.player_deck.value < self.opponent_deck.value:
            await self.db.update(itx.user.id, "-", self.amnt)

            embed = self.create_embed(
                color=0x9C1A36,
                description="Dealer has more than you. You lost :/",
                reveal_deck=True,
            )
        else:
            embed = self.create_embed(
                color=0x9C1A36,
                description="It's a tie!",
                reveal_deck=True,
            )

            balance = await self.db.get_balance(itx.user.id)

            embed.set_footer(text=f"Current balance: ${balance}")

        await itx.response.edit_message(
            embed=embed,
            view=None,
        )
        self.stop()


@commands.command(aliases=["bj"])
async def blackjack(ctx: commands.Context, amnt: MoneyConverterType):
    db: "Database" = ctx.bot.db

    await db.update(ctx.author.id, "-", amnt=amnt)  # hold the money hostage

    main_deck = []

    for suit in SUITS:
        for rank in RANKS:
            main_deck.append(Card(suit=suit, rank=rank))

    view = BlackJackView(
        main_deck=main_deck,
        player_deck=Deck(
            main_deck=main_deck,
            holder={
                "name": ctx.author.display_name,
                "user_id": ctx.author.id,
                "avatar_url": ctx.author.display_avatar.url,
            },
        ),
        amnt=amnt,
        db=db,
    )

    embed = view.create_embed(
        reveal_deck=False,
    )

    if view.player_deck.value >= 21 or view.opponent_deck.value >= 21:
        if view.player_deck.value > 21:
            if view.opponent_deck.value > 21:
                embed.color = 0x9C1A36
                embed.description = "You both **Bust**!"
            else:
                embed.color = 0x9C1A36
                embed.description = "You **Busted**!"
        elif view.opponent_deck.value > 21:
            embed.color = 0x9C1A36
            embed.description = "Dealer **Busted**!"
        elif view.player_deck.value == 21 and view.opponent_deck.value == 21:
            embed.color = 0x9C1A36
            embed.description = "It's a **Tie**!"
        elif view.player_deck.value == 21:
            embed.color = 0x32A852
            embed.description = f"**BLACKJACK!!** You have 21!"
        else:
            print(
                f"Unreachable player value: {view.player_deck.value}, dealer: {view.opponent_deck.value}"
            )

        view.stop()
        view = None

    view.message = await ctx.reply(  # type: ignore
        embed=embed,
        view=view,
    )


async def setup(bot: commands.Bot):
    bot.add_command(blackjack)
