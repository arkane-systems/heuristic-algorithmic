# Configuration data module

import configparser

# Global variables

_config = None


# functions - global configuration
def hal_bot_secret():
    """Get the Discord secret permitting bot login."""
    return (_config.get('hal', 'secret',
                        fallback=None))

def msg_level_debug():
    """Do we debug-log individual messages, or not?"""
    return _config.getboolean('hal', 'msg-level-debug', fallback=False)

# Initialization

def load():
    """Load the configuration from the config file ('/etc/genie.ini')."""
    global _config

    _config = configparser.ConfigParser()
    _config.read('hal.ini')