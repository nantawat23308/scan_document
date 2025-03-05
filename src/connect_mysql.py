import mysql.connector

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

class Connect_MySQL:

    def __init__(self, config_data):

        # connect mysql with maximum timeout
        self.connection = mysql.connector.connect(**config_data['general']['mysql_config'])

        # clear old data in mysql
        self._clear_old_data()

        # initialize parameter
        self.priority_file_format = config_data['md_conversion']['control_file_format']['priority']
        self.priority_pointer = 1
        self.priority_id_list = []
        self.pointer = 1

        self.query_batch_size = config_data['md_conversion']['mysql']['query_batch_size']
        self.getting_list = []
        
        self.insert_batch_size = config_data['md_conversion']['mysql']['insert_batch_size']
        self.sending_list = []
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def select_file(self):

        # select file from priority list
        if self.priority_file_format:
            data = self._priority_select_file()
            if data : return data

        # select file from normal list
        return self._normal_select_file()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def _priority_select_file(self):

        remove_priority = []

        # set priority query
        for file_format in self.priority_file_format:

            if not self.getting_list:

                query_priority = f"""
                    SELECT sf.id, sf.path, sf.name, sf.type
                    FROM test_meen.scan_folder sf
                    WHERE sf.type = '{file_format}'
                    AND sf.id >= {self.priority_pointer}
                    ORDER BY id
                    LIMIT {self.query_batch_size};
                """

                with self.connection.cursor() as cursor:
                    cursor.execute(query_priority)
                    self.getting_list = cursor.fetchall()

            data = self.getting_list.pop(0) if self.getting_list else None

            if data:

                self.priority_pointer = data[0] + self.query_batch_size

                self.priority_id_list.append(data[0])

                # remove non-existing priority formats
                for file_format in remove_priority:
                    self.priority_file_format.remove(file_format)

                return data
            
            else:

                self.priority_pointer = 1
                remove_priority.append(file_format)

        # remove non-existing priority formats
        self.priority_file_format = []

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def _normal_select_file(self):

        if not self.getting_list:

            # set normal query
            query = f"""
                SELECT sf.id, sf.path, sf.name, sf.type
                FROM test_meen.scan_folder sf
                WHERE sf.id >= {self.pointer}
                ORDER BY id
                LIMIT {self.query_batch_size};
            """

            # get data from mysql
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.getting_list = cursor.fetchall()

            self.pointer += self.query_batch_size

        data = self.getting_list.pop(0) if self.getting_list else None

        if data and (data[0] in self.priority_id_list):
            self.priority_id_list.remove(data[0])
            data = self._normal_select_file()

        return data if data else (None, None, None, None)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def batch_add_to_mysql(self, data = None, left_over = False):

        if not left_over:

            # add file into pending list
            self.sending_list.append(data)

            # add all file in pending list to mysql when length of pending list is equal batch size
            if len(self.sending_list) == self.insert_batch_size:
                self._add_to_mysql()
                self.sending_list = []

        else:

            # add all file in pending list to mysql for left over data
            if len(self.sending_list):
                self._add_to_mysql()
                self.sending_list = []

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def _add_to_mysql(self):

        # set query
        query = """
        INSERT INTO md_convert (id, path, name)
        VALUES (%s, %s, %s)
        """

        # set data for query
        values = [
            (
                data[0],
                data[1],
                data[2]
            )
            for data in self.sending_list
        ]

        # add data to mysql
        with self.connection.cursor() as cursor:
            cursor.executemany(query, values)
            self.connection.commit()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def close_connection(self):

        # close connection
        self.connection.close()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def _clear_old_data(self):
        
        # set query
        truncate_query = "TRUNCATE TABLE md_convert"

        # clear all values in mysql
        with self.connection.cursor() as cursor:
            cursor.execute(truncate_query)
            self.connection.commit()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
