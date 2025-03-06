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


def main(logger, file_input):
    scan_obj = DirectoryScan(logger)
    sql_obj = mysql_connection.MySqlConnector(
        **{"host": "172.17.106.183",
           "user": "root",
           "password": "1qaz2wsx",
           "database": "nantawats"}
    )
    cols = ['absolute_path', 'file_name', 'file_type', 'file_encode', 'file_size',
       'modified_time', 'file_permission', 'DIRorREGFILE', 'owner_uid',
       'owner_gid', 'name_owner', "md5"]
    count = 0
    data_batch = []
    time_start = time.time()
    for file_info in scan_obj.run_along(file_input):
        # push file_info
        count += 1
        data_batch.append(file_info)
        if len(data_batch) >= 10000:
            logger.debug(count)
            sql_obj.call_stored_procedure("insert_data_json", (json.dumps(data_batch), ))
            # sql_obj.insert_many_to_table(table_name="scan_dir", columns=cols, json_data=data_batch)
            data_batch.clear()
    if data_batch:
        sql_obj.call_stored_procedure("insert_data_json", (json.dumps(data_batch),))
        # sql_obj.insert_many_to_table(table_name="scan_dir", columns=cols, json_data=data_batch)
        data_batch.clear()

    logger.info(count)
    time_all = time.time() - time_start
    logger.info(time_all)
    print(time_all)



if __name__ == '__main__':
    # main("/")
    pass