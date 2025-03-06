import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

class MySqlConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.connection = None
        self.init_connection()
        self.cursor = self.connection.cursor()

    def init_connection(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    @classmethod
    def init_class_connection(cls, host, user, password, database):
        cls.host = host
        cls.user = user
        cls.password = password
        cls.database = database
        cls.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def init_create_database(cls, host, user, password, database):
        cls.host = host
        cls.user = user
        cls.password = password
        cls.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        cls.cursor = cls.connection.cursor()
        cls.create_database(database=database)


    @classmethod
    def create_database(cls, database):
        cls.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cls.connection.database = database
        cls.connection.commit()


    def modify_data(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def insert_to_table(self, table_name: str, columns: list, values: list) -> None:
        columns_name = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        sql = f"INSERT INTO {table_name} ({columns_name}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.connection.commit()


    def insert_many_to_table(self, table_name: str, columns: list, json_data: list[dict]) -> None:

        columns_name = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        sql = f"INSERT INTO {table_name} ({columns_name}) VALUES ({placeholders})"

        values = [tuple(data.values()) for data in json_data]
        for val in values:
            self.cursor.execute(sql, val)
        self.connection.commit()


    def create_table(self, table_name, columns: dict):
        """
        create table if not exists
        Args:
            table_name (str): name of table in database
            columns (dict): name of columns and data type

        Returns: None

        """
        key_type = ",".join([f"{key} {value}" for key, value in columns.items()])
        command = (
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (id BIGINT AUTO_INCREMENT PRIMARY KEY,{key_type})"""
                   )
        print(command)
        self.cursor.execute(command)
        self.connection.commit()

    def drop_table(self, table_name: str):
        command = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(command)
        self.connection.commit()

    def call_stored_procedure(self, procedure, data):
        self.cursor.callproc(procedure, args=data)
        self.connection.commit()



if __name__ == '__main__':
    conn = MySqlConnector(
        **{"host": "172.17.106.183",
            "user": "root",
            "password": "1qaz2wsx",
            "database": "nantawats"}
    )

    conn.drop_table("scan_dir")
    conn.create_table(table_name="scan_dir", columns={"absolute_path": "VARCHAR(255) NOT NULL",
                                                      "file_name": "VARCHAR(255)",
                                                      "file_type": "VARCHAR(255)",
                                                      "file_encode": "VARCHAR(255)",
                                                      "file_size": "BIGINT",
                                                      "modified_time": "DATETIME",
                                                      "file_permission": "VARCHAR(255)",
                                                      "DIRorREGFILE": "VARCHAR(255)",
                                                      'owner_uid': "SMALLINT",
                                                      "owner_gid": "SMALLINT",
                                                      "name_owner": "VARCHAR(255)",
                                                      "md5": "VARCHAR(255)"
                                                      })
