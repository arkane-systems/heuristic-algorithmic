# Core commands - basic commands present in every instance.

import discord
from discord.ext import commands
import logging

class Core(commands.Cog):
    """Core commands available to all users."""
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.core")
    
    @commands.command()
    async def ping(self, ctx):
        """Can you hear me, HAL? It's me, Dave."""
        self.logger.info('command invoked: ping')
        await ctx.send("pong")
