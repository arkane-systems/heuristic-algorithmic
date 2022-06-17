#! /usr/bin/env python3

# Fix up python search path.
import sys

sys.path.append('./deps')

# Imports

import discord
from discord.ext import commands
import logging
import semver

import __about__
import configuration
import helper

import cmd_core
import cmd_dev

# Bot class
class HeuristicAlgorithmic (commands.Bot):
    def __init__ (self, logger):

        self.logger = logger

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix='!',
                         description='Heuristic Algorithmic',
                         intents=intents,
                         activity=discord.Game(name="https://github.com/arkane-systems/heuristic-algorithmic"))

    async def setup_hook(self):
        # Add the commands in cogs to the system.
        await self.add_cog(cmd_core.Core(self))
        await self.add_cog(cmd_dev.Developer(self))

    async def on_command_error(self, ctx, exception):
        # Check for check failures.
        if isinstance (exception, commands.errors.CheckFailure):
            self.logger.info (f"User {ctx.author.name} is not permitted to run the command `{ctx.message.content}`.")
            await ctx.reply(f'You are not permitted to run the command `{ctx.message.content}`.')
            return

        await super().on_command_error(ctx, exception)

    async def on_message(self, message):
        # Do not process own messages.
        if message.author == bot.user:
            return

        # Perform message-level debug logging if it is enabled.
        if configuration.msg_level_debug is True:
            self.logger.debug("Message received: %s", message.content)

        # Default to processing bot commands.
        await self.process_commands (message)

    async def on_ready(self):
        # Log on successful login.
        self.logger.info('We have logged in as {0.user} (ID: {0.user.id})'.format(bot))

        # List the guilds we are members of.
        for guild in bot.guilds:
            self.logger.info ('Connected to guild {0.name} (ID: {0.id})'.format(guild))

# Non-class functions
def init_logging():
    """Set up top-level logging for the bot."""

    log_handler = logging.StreamHandler()
    log_handler.setFormatter (helper.ColorFormatter())
    logger = logging.getLogger('hal')
    logger.addHandler (log_handler)
    logger.setLevel (logging.DEBUG)

    return logger

def entrypoint():
    """Entry point of the application."""
    # Initialize logging
    logger = init_logging()

    # Load configuration.
    configuration.load()

    # Log basic information on startup.
    logger.info ("heuristic-algorithmic is starting up")
    logger.info ("heuristic-algorithmic version: %s", __about__.__version__)
    logger.info ("discord.py version: %s", discord.__version__)

    # Check if we have a secret.
    if configuration.hal_bot_secret() is None:
        logger.error ("no Discord bot secret specified; exiting")
        sys.exit (1)

    # Run the bot.
    global bot
    bot = HeuristicAlgorithmic(logger)
    bot.run (configuration.hal_bot_secret())

    # Log exit of entry point.
    logger.info ("heuristic-algorithmic is stopping")

entrypoint()
