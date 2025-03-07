import json
import os
import time
import logging
from src import libs
from src import mysql_connection
import stat


class DirectoryScan:
    def __init__(self, logger):
        self.logger = logger
        self.all_dir = []


    def walk_trough(self, top):
        for f in libs.list_all_inside(top):
            pathname = os.path.join(top, f)
            if not os.access(pathname, os.R_OK):
                continue
            mode = os.lstat(pathname).st_mode
            if stat.S_ISDIR(mode):
                # It's a directory, recurse into it
                self.all_dir.append(pathname)
                yield libs.get_file_metadata(pathname)
            elif stat.S_ISREG(mode):
                # It's a file, call the callback function
                yield libs.get_file_metadata(pathname)
            else:
                self.logger.info(f"skip {pathname}")

    def __que_folder(self):
        if self.all_dir:
            return self.all_dir.pop(0)
        else:
            return None

    def run_along(self, file_input):
        self.all_dir.append(file_input)
        while True:
            file_input = self.__que_folder()
            if not file_input:
                break
            yield from self.walk_trough(file_input)




if __name__ == '__main__':
    # main("/")
    pass