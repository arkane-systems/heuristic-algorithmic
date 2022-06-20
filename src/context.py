# Specialized context containing our own types.

import aiohttp
import discord
from discord.ext import commands
from typing import Union

from aiohttp import ClientSession
from pymongo.database import Database

class Context(commands.Context):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self) -> ClientSession:
        return self.bot.session

    @property
    def db(self) -> Database:
        return self.bot.db
