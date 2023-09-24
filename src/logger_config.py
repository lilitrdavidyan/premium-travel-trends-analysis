import os
import logging
from logging.handlers import RotatingFileHandler

# Create a logger object
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.INFO)

# Define the path for the log file
log_file_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'application.log')

# Create a file handler to write log messages to a file
file_handler = RotatingFileHandler(log_file_path, maxBytes=1e6, backupCount=5)  # 1e6 Bytes = 1 MB

# Create a formatter to specify the format of log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the file handler
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)



# This logger configuration will create a new log file every time the current log file reaches 1 MB in size and will keep the last 5 log files as backup. Older log files will have their filenames appended with a suffix like .1, .2, etc.


