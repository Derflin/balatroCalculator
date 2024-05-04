import logging

from config import INDENT

class AppFormatter(logging.Formatter):
    err_prefix_fmt = "ERROR: "
    warn_prefix_fmt = "WARNING: "

    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        # Prepare indent for the message based on context level
        indent_level = record.name.count(".")
        indent = INDENT * indent_level

        # Replace the original format with one customized by logging level
        fmt_orig = self._style._fmt
        if record.levelno == logging.ERROR:
            self._style._fmt = self.err_prefix_fmt + fmt_orig
        elif record.levelno == logging.WARNING:
            self._style._fmt = self.warn_prefix_fmt + fmt_orig

        # Call the original formatter class
        msg = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = fmt_orig

        # Apply prepared indent to every line of the formatted message
        return "\n".join([indent + line for line in msg.split("\n")])