import discord
from discord.ext import commands

from .converters import MoneyConverterType

class Embed(discord.Embed):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("color", 0x8662BD)
        super().__init__(*args, **kwargs)