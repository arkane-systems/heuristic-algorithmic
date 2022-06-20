#! /usr/bin/env python3

# Imports

import aiohttp
import discord
import logging
from discord.ext import commands
from context import Context
import pymongo
import traceback
from typing import Union

import __about__
import configuration
import helper

# Extension configuration
initial_extensions = (
    'cogs.core',
    'cogs.admin',
    'cogs.botadmin',
    'cogs.dev',
    'cogs.random',
)

# Bot class
class HeuristicAlgorithmic (commands.Bot):
    bot_app_info: discord.AppInfo
    config: configuration.Configuration
    connection: pymongo.MongoClient
    db: pymongo.database.Database
    logger: logging.Logger
    owner_id: int

    def __init__ (self, logger: logging.Logger, config: configuration.Configuration, connection: pymongo.MongoClient, db: pymongo.database.Database):

        self.logger = logger
        self.config = config
        self.connection = connection
        self.db = db

        intents = discord.Intents.default()
        intents.bans = True
        intents.members = True
        intents.messages = True
        intents.message_content = True
        intents.reactions = True

        super().__init__(command_prefix=commands.when_mentioned_or('!'),
                         description='Heuristic Algorithmic: a general-purpose Discord supervisor',
                         intents=intents,
                         activity=discord.Game(name="https://github.com/arkane-systems/heuristic-algorithmic"),
                         allowed_mentions=discord.AllowedMentions.all(),
                         chunk_guilds_at_startup=False,
                        )

    async def setup_hook(self) -> None:
        # Record self information
        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id

        # Maintain AIOHTTP client session
        self.session = aiohttp.ClientSession()

        # Add the commands in cogs to the system.
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                self.logger.info(f'Loaded extension {extension}.')
            except Exception as e:
                self.logger.error(f'Failed to load extension {extension}.')
                traceback.print_exc()

    async def start(self, token: str) -> None:
        await super().start(token, reconnect=True)

    async def close(self) -> None:
        # Close down AIOHTTP client session
        await self.session.close()
        await super().close()

    async def get_context(self, origin: Union[discord.Interaction, discord.Message], /, *, cls=Context) -> Context:
        """Deliver the custom context class instead of the default."""
        return await super().get_context(origin, cls=cls)

    async def on_command_error(self, ctx: Context, exception: commands.CommandError) -> None:
        # Check for check failures.
        if isinstance (exception, commands.CheckFailure):
            self.logger.info (f"User {ctx.author.name} is not permitted to run the command `{ctx.message.content}`.")
            await ctx.reply(f'You are not permitted to run the command `{ctx.message.content}`.')
        elif isinstance(exception, commands.NoPrivateMessage):
            await ctx.reply('This command cannot be used in private messages.')
        elif isinstance(exception, commands.DisabledCommand):
            await ctx.reply('Sorry. This command is disabled and cannot be used.')
        elif isinstance(exception, commands.MissingRequiredArgument):
            await ctx.reply(str(exception))
        elif isinstance(exception, commands.ArgumentParsingError):
            await ctx.reply(str(exception))
        elif isinstance(exception, commands.CommandInvokeError):
            if isinstance (exception.original, helper.NotYetImplemented):
                await ctx.reply("This command is not yet implemented.")
            else:
                await super().on_command_error(ctx, exception)
        else:
            await super().on_command_error(ctx, exception)

    async def on_message(self, message):
        # Do not process own messages.
        if message.author == self.user:
            return

        # Do not process bot messages unless configured otherwise.
        if (self.config.parse_bot_msgs() is False) and (message.author.bot is True):
            return

        # Perform message-level debug logging if it is enabled.
        if self.config.log_each_message() is True:
            self.logger.debug("Message received: %s", message.content)

        # Default to processing bot commands.
        await self.process_commands (message)

    async def on_ready(self):
        # Log on successful login.
        self.logger.info(f'We have logged in as {self.user} (ID: {self.user.id})')

        # Store the uptime (if the first call).
        if not hasattr (self, 'uptime'):
            self.uptime = discord.utils.utcnow()

        # Check for configs for our guilds; self-eject if there is wrongness.
        for guild in self.guilds:
            if self.config.does_guild_config_exist(guild.name):
                result = self.config.verify_guild_id (guild)

                if result == configuration.GuildVerified.VERIFIED:
                    self.logger.info (f'Successfully connected to guild {guild.name} (ID: {guild.id})')
                elif result == configuration.GuildVerified.UNVERIFIED:
                    self.logger.error (f'Incorrect ID specified for guild {guild.name}; self-ejecting.')
                    await guild.leave()
                else:
                    self.logger.warning (f'No id specified for guild {guild.name}; connecting anyway.')
            else:
                self.logger.error (f'No configuration exists for guild {guild.name}; self-ejecting.')
                await guild.leave()

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner
