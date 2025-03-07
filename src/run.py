import time
import json

def main(logger, scan_obj, my_sql_obj, file_input):
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
            my_sql_obj.call_stored_procedure("insert_data_json", (json.dumps(data_batch), ))
            # sql_obj.insert_many_to_table(table_name="scan_dir", columns=cols, json_data=data_batch)
            data_batch.clear()
    if data_batch:
        my_sql_obj.call_stored_procedure("insert_data_json", (json.dumps(data_batch),))
        # sql_obj.insert_many_to_table(table_name="scan_dir", columns=cols, json_data=data_batch)
        data_batch.clear()

    logger.info(count)
    time_all = time.time() - time_start
    logger.info(time_all)
    print(time_all)
