# Core commands - basic commands present in every instance.

import discord
from discord.ext import commands
import logging
import random

from helper import NotYetImplemented

class Core(commands.Cog):
    """Core commands available to all users."""
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.core")
    
    @commands.command()
    async def echo(self, ctx, *, message):
        """Repeat back a given message to you."""
        self.logger.info(f'command invoked: echo with parameters `{message}`')
        await ctx.reply (message)

    @commands.command(name='kill-all-humans')
    async def kill_all_humans(self, ctx):
        """Exactly what it says on the tin."""
        raise NotYetImplemented

    @commands.command()
    async def ping(self, ctx):
        """Can you hear me, HAL? It's me, Dave."""
        self.logger.info('command invoked: ping')
        await ctx.send("pong")

async def setup(bot):
    await bot.add_cog(Core(bot))

