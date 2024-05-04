import logging

from config import INDENT

class GameFormatter(logging.Formatter):
    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        msg = logging.Formatter.format(self, record)
        indent_level = record.name.count(".")
        indent = INDENT * indent_level
        return "\n".join([indent + line for line in msg.split("\n")])