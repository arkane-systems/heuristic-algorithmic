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

    @admin.command(name='get-special-channels')
    async def get_special_channels(self, ctx):
        """List the special channels available on this server."""
        self.logger.info('command invoked: admin get-special-channels')
        
        modchan = ctx.config.get_moderator_channel(ctx.guild)
        if modchan is not None:
            clist += f'Moderator channel: {modchan.name}\n'

        embed = discord.Embed(color=0x0000ff)
        embed.title = 'Special channels'
        embed.description = clist

        await ctx.send(embed=embed, reference=ctx.message)

async def setup(bot):
    await bot.add_cog(Administration(bot))
