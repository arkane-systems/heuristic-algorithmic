# Developer commands - commands for further developing this bot.

import discord
from discord.ext import commands
import logging

class Developer(commands.Cog, command_attrs=dict(hidden=True)):
    """For the further development of this bot."""
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger.getChild("commands.developer")

    async def cog_check(self, ctx):
        """Only the bot owner can use these commands."""
        valid = await self.bot.is_owner (ctx.author)
        self.logger.debug (f"is owner? {valid}")
        return valid

    @commands.command()
    async def get_guild_id(self, ctx):
        """Display the ID of the current guild (server)."""
        self.logger.info('command invoked: get_guild_id')
        await ctx.reply(f"ID of the current guild {ctx.guild.name} is {ctx.guild.id}.")

    @commands.command()
    async def get_channel_id(self, ctx):
        """Display the ID of the current channel."""
        self.logger.info('command invoked: get_channel_id')
        await ctx.reply(f"ID of the current channel #{ctx.channel.name} is {ctx.channel.id}.")

    @commands.command()
    async def get_my_id(self, ctx):
        """Display the ID of the invoking user."""
        self.logger.info('command invoked: get_my_id')
        await ctx.reply(f"Current user with name {ctx.author.name} and nick {ctx.author.nick} is {ctx.author.id}.")

async def setup(bot):
    await bot.add_cog(Developer(bot))
