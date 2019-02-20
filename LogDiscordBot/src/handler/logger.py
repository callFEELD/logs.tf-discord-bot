# last edit: 20.02.2019 (callFEELD)
import logging

from src.handler.config import config

LOGGING_LEVEL_CONSOLE = logging.DEBUG
LOGGING_LEVEL_FILE = LOGGING_LEVEL_CONSOLE
LOG_FILE = config["Paths"]["log"]
LOG_FILE_MODE = 'a'
LOG_FORMAT = '[%(levelname)s] %(asctime)s - %(message)s'

logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT)
logger = logging.getLogger('Log-Discord-Bot')
logger.setLevel(LOGGING_LEVEL_CONSOLE)

# File Handler
file_handler = logging.FileHandler(LOG_FILE, mode=LOG_FILE_MODE)
file_handler.setLevel(LOGGING_LEVEL_FILE)


# create formatter and add it to the handlers
formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)