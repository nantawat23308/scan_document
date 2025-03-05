import os
import sys
import argparse
import json
import traceback
from datetime import datetime

from ottools import otcommon, otdatetime

from src import mysql_connection, utility
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def process_main():
    '''
    Runs the main process
    
    Args: 
    '''

    global config_data, logger

    main_tracker = otdatetime.TimeTracker()
    main_tracker.start()
    logger.info(f"START: process_main - Start: {main_tracker.start_time_formatted}")

    # Initialize Object
    mysql_conn = mysql_connection.MySqlConnector(**config_data)



    
    pass

    # Start Processing
    
    try:

        pass

    except Exception as e:

        # print when code error
        error_info = traceback.format_exc()
        print(error_info)

    finally:

        pass

    # End Processing
    main_tracker.stop()
    logger.info(f"END: process_main - Start: {main_tracker.start_time_formatted} End: {main_tracker.end_time_formatted} Duration: {main_tracker.duration_formatted}")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def init(args):
    '''
    Initializes the module for running
    '''

    global config_data, logger

    #####################
    ## Start the logger
    #####################

    # Generate the log file name. This name will be used throughout the process, even if the date rolls over. 
    # The name is based on the start time of the process.

    # Read the config JSON
    with open(args.config_file_path, 'r', encoding='utf-8') as config_file:
        config_data = json.load(config_file)

    # Create the full log file path
    log_folder_path = config_data['general']['log_folder_path']
    log_file_name = datetime.now().strftime("%Y%m%d") + "-scan_folder.log"
    log_file_path = os.path.join(log_folder_path, log_file_name)
        
    # Initialize the logger
    logger, file_handler = otcommon.configure_logger(log_file_path)
    logger.info(f"Logging to {log_file_path}")

    #####################
    ## Initalize
    #####################

    logger.info(f"Initialize complete - Begin processing")

    #Initialize complete - Begin processing  
    process_main()

    # clear logging after finished
    otcommon.cleanup_logger(logger, file_handler)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def validate_args(args):

    # Validate the files and paths
    if not args.config_file_path:
        raise ValueError(f"config_file_path is required.")

    if not os.path.exists(args.config_file_path):
        raise ValueError(f"config_file_path does not exist.")

    # All validations passed
    return 

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def configure_parser():

    parser = argparse.ArgumentParser(description='Wrapper process for processing an folder')

    if otcommon.is_debugging(): # otcommon.is_debugging()
        parser.add_argument('--config_file_path', type=str, help='The config file', default="config/config.json")
        parser.add_argument('--verbose', type=bool, help='Enables verbose logging. Prints contents sent to the log file to the screen', default=True)        
        parser.add_argument('--debug_mode', type=bool, help='Enables debug mode.', default=False)

    else:
        parser.add_argument('--config_file_path', type=str, help='The config file', required=True, default="config.json")
        parser.add_argument('--verbose', type=bool, help='Enables verbose logging. Prints contents sent to the log file to the screen', default=False)        
        parser.add_argument('--debug_mode', type=bool, help='Enables debug mode.', default=False)

    return parser

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    '''
    The main rountine to start the module. 
    '''

    parser = configure_parser()
    args = parser.parse_args()
    
    try:
        validate_args(args)
        # Initialize and prepare to run
        init(args)

    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

    # Normal Exit
    sys.exit()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    main()

