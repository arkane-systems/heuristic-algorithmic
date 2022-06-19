# HAL Administrator commands - commands for bot administrators.

import discord
from discord.ext import commands
import logging

from bot import HeuristicAlgorithmic

class Hal(commands.Cog):
    bot: HeuristicAlgorithmic

    """HAL administration commands (bot owner only)."""
    def __init__(self, bot: HeuristicAlgorithmic):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.botadmin")

    async def cog_check(self, ctx):
        """Only the bot owner can use these commands."""
        valid = await self.bot.is_owner (ctx.author)
        self.logger.debug (f"is owner? {valid}")
        return valid

    @commands.group()
    async def hal(self, ctx):
        """'bot administration commands; !help hal for details."""
        if ctx.invoked_subcommand is None:
            await ctx.reply('You must specify a subcommand to `hal`.')

    @hal.command()
    async def shutdown(self, ctx):
        """Shut down the bot (this command affects all servers)."""
        self.logger.info('command invoked: hal shutdown')
        await ctx.reply('Heuristic Algorithmic is shutting down...')
        await self.bot.close()

async def setup(bot: HeuristicAlgorithmic):
    await bot.add_cog(Hal(bot))
