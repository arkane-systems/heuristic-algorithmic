# Random commands - commands powered by randomness and chaos.

import discord
from discord.ext import commands
import logging
import random

from context import Context
from helper import NotYetImplemented

class Random(commands.Cog):
    """Commands powered by randomness and chaos."""
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.random")

    @commands.command()
    async def dog(self, ctx: Context):
        """Display a randomly chosen dog picture."""
        self.logger.info('command invoked: dog')

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
