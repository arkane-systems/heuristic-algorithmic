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
        intents.guild_reactions = True

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

    async def on_message_delete(self, message: discord.Message):
        # If configured to do so, echo deleted messages on the moderator channel.
        if message.guild is not None:
            if self.config.show_mods_deletes(message.guild) is True:
                msg = f'**@{message.author}, in channel #{message.channel.name}, has deleted the message:**\n\n{message.content}'
                modchan = self.config.get_moderator_channel(message.guild)

                if modchan is None:
                    self.logger.error ("Cannot echo deleted message; moderator channel not configured.")

                await modchan.send(msg, allowed_mentions=discord.AllowedMentions.none())

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        # If configured to do so, echo edited messages on the moderator channel.
        if before.guild is not None:
            if self.config.show_mods_deletes(before.guild) is True:
                msg = f'**@{before.author}, in channel #{before.channel.name}, has edited their message:**\n\n{before.content}\n\n**to read:**\n\n{after.content}'
                modchan = self.config.get_moderator_channel(before.guild)

                if modchan is None:
                    self.logger.error ("Cannot echo edited message; moderator channel not configured.")

                await modchan.send(msg, allowed_mentions=discord.AllowedMentions.none())

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        user = payload.member
        emoji = payload.emoji.name

        if emoji == '📌':
            # Handle pin reactions.
            guild = self.get_guild (payload.guild_id)
            threshold = self.config.autopin_threshold(guild)

            if threshold == 0:
                # Autopinning is disabled.
                return
            
            pinchan = self.config.get_autopin_channel(guild)
            channel = self.get_channel (payload.channel_id)

            if channel == pinchan:
                self.logger.info (f"Pin added to message in {guild}'s autopin channel; ignoring.")
                return

            # Get the message.
            message = await channel.fetch_message (payload.message_id)

            # Check for pinability; count reactions
            pincount = discord.utils.find(lambda r: r.emoji == '📌', message.reactions).count
            by_admin = user.guild_permissions.administrator

            self.logger.info (f'Pin added to message on #{channel}@{guild} by {user}; count = {pincount}; by_admin={by_admin}')

            if (pincount >= threshold) or by_admin:
                # Pin the message.
                await self.pin_message (message)

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

    async def pin_message(self, message: discord.Message):
        # Check for duplicates so we don't pin the same message twice.
        result = self.db['pin'].find_one ({ 'guild_id' : message.guild.id, 'message_id' : message.id })

        if result is not None:
            self.logger.info ("No need to pin message; it has already been pinned.")
            return

        # Pin the message.
        author = message.author.name
        originalchan = message.channel.name

        self.logger.info (f'Pinning message {message.id} to highlights channel (from @{author} on #{originalchan}).')

        content = f'**@{author} said on channel #{originalchan}:**\n' + message.content
        attachments = message.attachments
        embeds = []

        for att in attachments:
            embeds.append(discord.Embed(title=att.name,url=att.url))

        highchan = self.config.get_autopin_channel(message.guild)
        await highchan.send (content, embeds=embeds)

        # Record the pinning of the message.
        self.db['pin'].insert_one ({ 'guild_id' : message.guild.id, 'message_id' : message.id })

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner
