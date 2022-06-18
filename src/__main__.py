#! /usr/bin/env python3

# Fix up python search path.
import sys

sys.path.append('./deps')

# Imports

import aiohttp
import asyncio
import discord
from discord.ext import commands
from context import Context
import logging
import semver
from typing import Union

import __about__
from bot import HeuristicAlgorithmic
import configuration
import helper

# Startup functions
def init_logging():
    """Set up top-level logging for the bot."""

    log_handler = logging.StreamHandler()
    log_handler.setFormatter (helper.ColorFormatter())
    logger = logging.getLogger('hal')
    logger.addHandler (log_handler)
    logger.setLevel (logging.DEBUG)

    return logger

async def run_bot(logger):
    bot = HeuristicAlgorithmic(logger)
    await bot.start(configuration.hal_bot_secret())


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
    asyncio.run(run_bot(logger))

    # Log exit of entry point.
    logger.info ("heuristic-algorithmic is stopping")

entrypoint()
