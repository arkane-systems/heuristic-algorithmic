# Administrator commands - commands for server administrators.

import discord
from discord.ext import commands
import logging

class Administration(commands.Cog):
    """Server administration commands (administrators only)."""
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.administration")

    async def cog_check(self, ctx):
        """Only a server administrator can use these commands."""
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        
        self.logger.debug (f"is server administrator? {ctx.author.guild_permissions.administrator}")
        return ctx.author.guild_permissions.administrator

    @commands.group()
    async def admin(self, ctx):
        """server administration commands; !help admin for details."""
        if ctx.invoked_subcommand is None:
            await ctx.reply('You must specify a subcommand to `admin`.')
