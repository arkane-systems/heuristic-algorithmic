# Template - insert description here.

import discord
from discord.ext import commands
import logging
import random

from bot import HeuristicAlgorithmic
from context import Context

class Template(commands.Cog):
    bot: HeuristicAlgorithmic

    """Insert description of commands here."""
    def __init__(self, bot: HeuristicAlgorithmic):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.template")

async def setup(bot):
    await bot.add_cog(Template(bot))
