# Configuration data module

import copy
import os.path
import sys
import yaml

class Configuration:
    configData: dict

    def __init__(self):
        try:
            with open (os.path.join (os.path.dirname(__file__), 'config.yaml'), "r") as yamlfile:
                self.configData = yaml.safe_load (yamlfile)
        except:
            print ("error reading configuration file.")
            sys.exit(2)

    def get_config_dump(self) -> str:
        """Get the actual config as parsed, as a string."""
        dump_data = copy.deepcopy(self.configData)

        # Censor secrets in dump.
        dump_data['global']['discordSecret'] = '<censored>'
        dump_data['global']['database']['connectionString'] = '<censored>'

        return yaml.dump(dump_data)

    # Globals
    def discord_secret(self) -> str:
        """Get the Discord secret permitting bot login."""
        if 'global' in self.configData:
            if 'discordSecret' in self.configData['global']:
                value = self.configData['global']['discordSecret']

                if isinstance(value, str):
                    return value

        return None

    ## Database
    def mongodb_connection(self) -> str:
        """Get the mongodb connection string for the back-end database."""
        if 'global' in self.configData:
            if 'database' in self.configData['global']:
                if 'connectionString' in self.configData['global']['database']:
                    value = self.configData['global']['database']['connectionString']

                    if isinstance(value,str):
                        return value

        return None

    def mongodb_db_name(self) -> str:
        """Get the mongodb database name for the back-end database."""
        if 'global' in self.configData:
            if 'database' in self.configData['global']:
                if 'connectionString' in self.configData['global']['database']:
                    value = self.configData['global']['database']['databaseName']

                    if isinstance(value,str):
                        return value

        return None

    ## Logging
    def log_each_message(self) -> bool:
        """Log every Discord message received, or not?"""
        if 'global' in self.configData:
            if 'logging' in self.configData['global']:
                if 'logMessages' in self.configData['global']['logging']:
                    value = self.configData['global']['logging']['logMessages']

                    if isinstance(value,bool):
                        return value

        return False

    ## Options
    def parse_bot_msgs(self) -> bool:
        """Parse messages from other bots, or not?"""
        if 'global' in self.configData:
            if 'options' in self.configData['global']:
                if 'parseBotMessages' in self.configData['global']['options']:
                    value = self.configData['global']['options']['parseBotMessages']

                    if isinstance(value,bool):
                        return value

        return False

    # Guilds
    

