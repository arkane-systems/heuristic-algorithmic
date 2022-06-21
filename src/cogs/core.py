# Core commands - basic commands present in every instance.

import discord
from discord.ext import commands
import os
import sys

import __about__
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
    async def about(self, ctx):
        """Display information about the bot."""
        self.logger.info(f'command invoked: about')
        
        embed = discord.Embed(title='About The Bot', type='rich', color=0x0000ff)
        embed.set_author (name=f'Heuristic Algorithmic ({__about__.__version__})',
                          url='https://github.com/arkane-systems/heuristic-algorithmic',
                          icon_url='https://raw.githubusercontent.com/arkane-systems/heuristic-algorithmic/master/hal_eye.jpg')

        # Latency
        # Memory
        # Messages Seen
        # Presence
        # Up Time

        embed.add_field(name='**Author**', value='Cerebrate#5337', inline=True)
        embed.add_field(name='**Owner**', value=self.bot.owner.name, inline=True)

        embed.add_field(name='**Library**', value=f'discordpy ({discord.__version__})', inline=False)
        embed.add_field(name='**OS**', value=os.uname().release, inline=False)
        embed.add_field(name='**Python**', value=sys.version, inline=False)
        embed.add_field(name='**Website**', value='https://github.com/arkane-systems/heuristic-algorithmic', inline=False)
        embed.add_field(name='**Terms of Service**', value='By joining a server using this bot or adding this bot to your server, you give express permission for the bot to collect and store any information it deems necessary to perform its functions, including but not limited to message content, message metadata, and user metadata.', inline=False)

        await ctx.send (content="", embed=embed, reference=ctx.message)

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

