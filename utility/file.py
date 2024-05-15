import logging
import json
import time

from config import DEFAULT_SAVE_DIRECTORY

class JsonFile:
    def __init__(self, file_name):
        self.__setLoggers__()

        # Set default file name and extension if they weren't provided
        self.file_name = file_name
        if self.file_name is None:
            self.file_name = "save_" + time.strftime("%Y%m%d-%H%M%S") + ".json"
        elif not self.file_name.endswith(".json"):
            self.file_name += ".json"

        # Set file parent directory based on what was provided through file name
        self.file_dir_path = ""
        if "/" not in self.file_name:
            self.file_dir_path = DEFAULT_SAVE_DIRECTORY
        else:
            path = self.file_name.rsplit("/", maxsplit=1)
            self.file_dir_path = path[0] + "/"
            self.file_name = path[1]

    def __setLoggers__(self):
        # Set logger for current object
        self.logger = logging.getLogger(__name__)

    def read(self):
        parsed_data = None
        try:
            with open(self.file_dir_path + self.file_name, "r", encoding='utf-8') as file:
                parsed_data = json.load(file)
            self.logger.info(F"Successfully read data from file called \"{self.file_name}\" in \"{self.file_dir_path}\"")
        except FileNotFoundError:
            self.logger.error(F"Couldn't find file called \"{self.file_name}\" in \"{self.file_dir_path}\"")
            return None
        except PermissionError:
            self.logger.error(F"Don't have adequate permissions to read file called \"{self.file_name}\" in \"{self.file_dir_path}\"")
            return None

        return parsed_data

    def write(self, data):
        try:
            with open(self.file_dir_path + self.file_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            self.logger.info(F"Successfully written data to file called \"{self.file_name}\" in \"{self.file_dir_path}\"")
        except PermissionError:
            self.logger.error(F"Don't have adequate permissions to create or modify file called \"{self.file_name}\" in \"{self.file_dir_path}\"")
            return None
        
        return self.file_name
    