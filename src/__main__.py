#! /usr/bin/env python3

# Fix up python search path.
import sys

sys.path.append('deps')

# Imports

import discord
import logging
import semver

import __about__

# Constants
discord_version = semver.VersionInfo (discord.version_info.major, discord.version_info.minor, discord.version_info.micro)

# Globals
logger = None

# Core Functions
def init_logging():
    """Set up logging for the bot."""
    global logger

    logging.basicConfig (level=logging.INFO)
    logger = logging.getLogger ('hal')

# Entrypoint
def entrypoint():
    """Entry point of the application."""

    # Set up and configure logging.
    init_logging()

    # Log basic information on startup.
    logger.info ("heuristic-algorithmic is starting up")
    logger.info ("heuristic-algorithmic version: %s", __about__.__version__)
    logger.info ("discord.py version: %s", discord_version)

    # Log exit of entry point.
    logger.info ("heuristic-algorithmic is stopping")

entrypoint()
