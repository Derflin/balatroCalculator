import logging
import json
import zlib
import time
import re

from config import DEFAULT_SAVE_DIRECTORY

class File:
    def __init__(self, file_name, default_file_name, default_file_extension):
        self.__setLoggers__()
        
        # Set default file name and extension if they weren't provided
        self.file_name = file_name
        if self.file_name is None:
            self.file_name = default_file_name + default_file_extension
        elif not self.file_name.endswith(default_file_extension):
            self.file_name += default_file_extension

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
        pass

    def write(self, data):
        pass

class JsonFile(File):
    def __init__(self, file_name):
        # Initialize parent
        default_file_name = "save_" + time.strftime("%Y%m%d-%H%M%S")
        default_file_extension = ".json"
        super().__init__(file_name, default_file_name, default_file_extension)

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
    
class JkrFile(File):
    def __init__(self, file_name):
        # Initialize parent
        default_file_name = "save"
        default_file_extension = ".jkr"
        super().__init__(file_name, default_file_name, default_file_extension)

        # Set map to translate JKR format to JSON
        self.map_json = {
            '["': '"',
            '"]': '"',
            ',}': '}',
            '=': ':',
            '[': '"',
            ']': '"',
            '\\"': '"',
        }
        self.map_json = dict((re.escape(k), v) for k, v in self.map_json.items())
        self.pattern_json = re.compile("|".join(self.map_json.keys()))

    def __setLoggers__(self):
        # Set logger for current object
        self.logger = logging.getLogger(__name__)

    def read(self):
        try:
            with open(self.file_dir_path + self.file_name, "rb") as file:
                compressed_data = file.read()
            self.logger.info(F"Successfully read data from file called \"{self.file_name}\" in \"{self.file_dir_path}\"")
        except FileNotFoundError:
            self.logger.error(F"Couldn't find file called \"{self.file_name}\" in \"{self.file_dir_path}\"")
            return None
        except PermissionError:
            self.logger.error(F"Don't have adequate permissions to read file called \"{self.file_name}\" in \"{self.file_dir_path}\"")
            return None
        
        parsed_data = str(zlib.decompress(compressed_data, wbits=-15, bufsize=16384))
        parsed_data = parsed_data.lstrip("b'return ").rstrip("'")
        parsed_data = self.pattern_json.sub(lambda m: self.map_json[re.escape(m.group(0))], parsed_data)
        parsed_data = json.loads(parsed_data)

        return parsed_data
