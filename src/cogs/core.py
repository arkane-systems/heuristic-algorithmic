# Core commands - basic commands present in every instance.

import discord
from discord.ext import commands
import logging
import random

from bot import HeuristicAlgorithmic
from context import Context
from configuration import Configuration
from helper import NotYetImplemented

class Core(commands.Cog):
    bot: HeuristicAlgorithmic

    """Core commands available to all users."""
    def __init__(self, bot: HeuristicAlgorithmic):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.core")

    @commands.command()
    async def echo(self, ctx, *, message):
        """Repeat back a given message to you."""
        self.logger.info(f'command invoked: echo with parameters `{message}`')
        await ctx.reply(message)

    @commands.command()
    async def hello(self, ctx: Context):
        """Displays my intro message."""
        await ctx.reply('Hello! I\'m a robot! Cerebrate#5337 made me to administer his servers.')

    @commands.command(name='kill-all-humans')
    async def kill_all_humans(self, ctx):
        """Exactly what it says on the tin."""
        raise NotYetImplemented

    @commands.command()
    async def ping(self, ctx):
        """Can you hear me, HAL? It's me, Dave."""
        self.logger.info('command invoked: ping')
        await ctx.send("pong")

    @commands.command()
    async def rtfaq(self, ctx):
        """Send a link to the server FAQ."""
        self.logger.info('command invoked: rtfaq')

        faqurl = ctx.config.get_faq_url(ctx.guild)

        if faqurl is None:
            await ctx.reply('No FAQ is configured for this server, sorry.')
            return

        ref = ctx.message

        if ctx.message.reference is not None:
            ref = ctx.message.reference

        faqembed = discord.Embed(title="Server FAQ", type='link', url=faqurl, color=0x0000ff)

        await ctx.send(content="Further information on this topic is available in the server FAQ:",
                       embed=faqembed, reference=ref)

async def setup(bot):
    await bot.add_cog(Core(bot))

