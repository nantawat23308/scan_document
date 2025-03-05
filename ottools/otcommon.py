import os
import sys
import logging
import logging.handlers
import queue

##############################
## Logger functions
##############################

## Global Variables
logger_initialized = False
log_queue = queue.Queue()
queue_handler = logging.handlers.QueueHandler(log_queue)

def is_debugging():
    # Checks if any of 'gettrace' returns a non-None value (common way to detect debuggers)
    if sys.gettrace() is not None:
        return True
    return False

def configure_logger(log_path, verbose=False):
    global logger_initialized, log_file_path, log_verbose, logger

    if logger_initialized:
        return

    log_verbose = verbose #### TODO - handle verbose
    log_file_path = log_path
    logger = logging.getLogger('globalLogger')
    logger.setLevel(logging.DEBUG)

    # Set up the console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)

    # Set up the file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    # Set up the queue listener with the console and file handlers
    queue_listener = logging.handlers.QueueListener(log_queue, console_handler, file_handler)
    queue_listener.start()

    # Add the queue handler to the logger
    logger.addHandler(queue_handler)

    logger_initialized = True
    return logger, file_handler

def cleanup_logger(logger, file_handler):
    if file_handler:
        file_handler.close()  # Close the file handler
        logger.removeHandler(file_handler)  # Remove the handler from the logger


def clear_folder(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.error(f"Failed to delete {file_path}. Reason: {e}")