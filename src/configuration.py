# Configuration data module

import configparser
from xmlrpc.client import Boolean

# Global variables

_config = None


# functions - global configuration
def hal_bot_secret() -> str:
    """Get the Discord secret permitting bot login."""
    return (_config.get('hal', 'secret',
                        fallback=None))

def mongodb_connection() -> str:
    """Get the mongodb connection string for the back-end database."""
    return _config.get('hal', 'mongodb-connection', fallback=None)

def mongodb_db_name() -> str:
    """Get the mongodb database name for the back-end database."""
    return _config.get('hal', 'mongodb-database', fallback='hal')

def msg_level_debug() -> bool:
    """Do we debug-log individual messages, or not?"""
    return _config.getboolean('hal', 'msg-level-debug', fallback=False)

def parse_bot_msgs() -> bool:
    """Do we parse messages from other bots, or not?"""
    return _config.getboolean('hal', 'parse-bot-msgs', fallback=False)

# Initialization

def load():
    """Load the configuration from the config file ('/etc/genie.ini')."""
    global _config

    _config = configparser.ConfigParser()
    _config.read('hal.ini')