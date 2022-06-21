#! /usr/bin/env python3

# Fix up python search path.
from multiprocessing import connection
import os.path
import sys

sys.path.append(os.path.join (os.path.dirname(__file__), 'deps'))

# Imports

import aiohttp
import asyncio
import discord
from discord.ext import commands
from context import Context
import logging
import pymongo
from typing import Union

import __about__
from bot import HeuristicAlgorithmic
import configuration
import helper

def init_logging() -> logging.Logger:
    """Set up top-level logging for the bot."""

    log_handler = logging.StreamHandler()
    log_handler.setFormatter (helper.ColorFormatter())
    logger = logging.getLogger('hal')
    logger.addHandler (log_handler)
    logger.setLevel (logging.DEBUG)

    return logger


def init_database(logger: logging.Logger, config: configuration.Configuration) -> pymongo.MongoClient:
    """Set up connection to the MongoDB back-end."""
    connection = pymongo.MongoClient(config.mongodb_connection())

    try:
        # The ping command is cheap and does not require auth.
        connection.admin.command('ping')
    except pymongo.errors.ConnectionFailure:
        logger.critical ("mongodb back-end not available.")
        sys.exit(1)

    return connection


def prepare_database(logger: logging.Logger, config: configuration.Configuration, connection: pymongo.MongoClient) -> pymongo.database.Database:
    """Prepare the HAL database for use."""
    db_name = config.mongodb_db_name()

    # Check if it exists.
    dbs = connection.list_database_names()
    if db_name in dbs:
        # Return existing one.
        return connection[db_name]
    else:
        # Create database.
        db = connection.get_database(db_name)

        # Create meta collection.
        meta = db.create_collection ('meta')
        meta.create_index ('name', unique=True)

        # Write creation date.   
        meta.insert_one ({'name' : 'created', 'time' : discord.utils.utcnow()})

        # Create pin collection.
        pin = db.create_collection ('pin')
        pin.create_index ([('guild_id', pymongo.ASCENDING), ('message_id', pymongo.ASCENDING)],
            unique = True)

        # TODO: schemata/validation rules

        # TODO: write default values?

        # And return.
        return db


async def run_bot(logger: logging.Logger, config: configuration.Configuration, connection: pymongo.MongoClient, db: pymongo.database.Database):
    bot = HeuristicAlgorithmic(logger, config, connection, db)
    await bot.start(config.discord_secret())


def entrypoint():
    """Entry point of the application."""
    # Initialize logging
    logger = init_logging()

    # Load configuration.
    config = configuration.Configuration()

    # Log basic information on startup.
    logger.info ("heuristic-algorithmic is starting up")
    logger.info ("heuristic-algorithmic version: %s", __about__.__version__)
    logger.info ("discord.py version: %s", discord.__version__)

    # Initialize database
    connection = init_database (logger, config)

    # Prepare database
    db = prepare_database (logger, config, connection)

    # Check if we have a secret.
    if config.discord_secret() is None:
        logger.error ("no Discord bot secret specified; exiting")
        sys.exit (1)

    # Run the bot.
    asyncio.run(run_bot(logger, config, connection, db))

    # Log exit of entry point.
    logger.info ("heuristic-algorithmic is stopping")

    # Close database connection.
    connection.close()

entrypoint()
