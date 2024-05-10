import logging
import json
import time

from config import DEFAULT_SAVE_DIRECTORY

class JsonFile:
    def __init__(self, filename):
        self.__setLoggers__()

        self.filename = filename
        if self.filename is None:
            self.filename = "save_" + time.strftime("%Y%m%d-%H%M%S") + ".json"
        elif not self.filename.endswith(".json"):
            self.filename += ".json"

    def __setLoggers__(self):
        # Set logger for current object
        self.logger = logging.getLogger(__name__)

    def readJson(self):
        parsed_data = None
        try:
            with open(DEFAULT_SAVE_DIRECTORY + self.filename, "r", encoding='utf-8') as file:
                parsed_data = json.load(file)
            self.logger.info(F"Successfully read data from file called \"{self.filename}\" in \"{DEFAULT_SAVE_DIRECTORY}\"")
        except FileNotFoundError:
            self.logger.error(F"Couldn't find file called \"{self.filename}\" in \"{DEFAULT_SAVE_DIRECTORY}\"")
            return None
        except PermissionError:
            self.logger.error(F"Don't have adequate permissions to read file called \"{self.filename}\" in \"{DEFAULT_SAVE_DIRECTORY}\"")
            return None

        return parsed_data

    def writeJson(self, data):
        try:
            with open(DEFAULT_SAVE_DIRECTORY + self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            self.logger.info(F"Successfully written data to file called \"{self.filename}\" in \"{DEFAULT_SAVE_DIRECTORY}\"")
        except PermissionError:
            self.logger.error(F"Don't have adequate permissions to create or modify file called \"{self.filename}\" in \"{DEFAULT_SAVE_DIRECTORY}\"")
            return None
        
        return self.filename