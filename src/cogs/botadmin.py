# HAL Administrator commands - commands for bot administrators.

import discord
from discord.ext import commands
import logging

class HalAdministration(commands.Cog):
    """HAL administration commands (bot owner only)."""
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.botadmin")

    async def cog_check(self, ctx):
        """Only the bot owner can use these commands."""
        valid = await self.bot.is_owner (ctx.author)
        self.logger.debug (f"is owner? {valid}")
        return valid

    @commands.group()
    async def botadmin(self, ctx):
        """'bot administration commands; !help botadmin for details."""
        if ctx.invoked_subcommand is None:
            await ctx.reply('You must specify a subcommand to `admin`.')

    @botadmin.command()
    async def shutdown(self, ctx):
        """Shut down the bot (this command affects all servers)."""
        self.logger.info('command invoked: botadmin shutdown')
        await ctx.reply('Heuristic Algorithmic is shutting down...')
        await self.bot.close()
