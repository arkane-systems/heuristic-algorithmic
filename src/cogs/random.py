# Random commands - commands powered by randomness and chaos.

import discord
from discord.ext import commands
import logging
import random

from bot import HeuristicAlgorithmic
from context import Context
from helper import NotYetImplemented

class Random(commands.Cog):
    """Commands powered by randomness and chaos."""
    bot: HeuristicAlgorithmic

    def __init__(self, bot: HeuristicAlgorithmic):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.random")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='\N{GAME DIE}')

    @commands.group()
    async def random(self, ctx: Context):
        """Displays a random thing you request; !help random for details."""
        if ctx.invoked_subcommand is None:
            await ctx.reply(f'You must specify a subcommand to `random`.')

    @random.command()
    async def dog(self, ctx: Context):
        """Display a randomly chosen dog picture."""
        self.logger.info('command invoked: random dog')

        async with ctx.session.get('https://random.dog/woof') as resp:
            if resp.status != 200:
                return await ctx.reply('No dog found :(')

            filename = await resp.text()
            url = f'https://random.dog/{filename}'
            filesize = ctx.guild.filesize_limit if ctx.guild else 8388608

            if filename.endswith(('.mp4', '.webm')):
                async with ctx.typing():
                    async with ctx.session.get(url) as other:
                        if other.status != 200:
                            return await ctx.reply('Could not download dog video :(')

                        if int(other.headers['Content-Length']) >= filesize:
                            return await ctx.reply(f'Video was too big to upload... See it here: {url} instead.')

                        fp = io.BytesIO(await other.read())
                        await ctx.send(file=discord.File(fp, filename=filename, reference=ctx.message))

            else:
                await ctx.send(embed=discord.Embed(title='Random Dog').set_image(url=url), reference=ctx.message)

    @random.command()
    async def number(self, ctx: Context, minimum: int = 0, maximum: int = 100):
        """Displays a random number within an optional range.
        The minimum must be smaller than the maximum and the maximum number
        accepted is 1000.
        """
        self.logger.info('command invoked: random number')

        maximum = min(maximum, 1000)
        if minimum >= maximum:
            await ctx.reply('Maximum is smaller than minimum.')
            return

        await ctx.reply(str(random.randint(minimum, maximum)))

async def setup(bot):
    await bot.add_cog(Random(bot))
