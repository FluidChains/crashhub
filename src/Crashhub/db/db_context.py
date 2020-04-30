# Crashhub/db/db_context.py
import psycopg2

class PostgresConfig:

    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.conn = None

    def return_connection(self): 
        if self.conn:
            return self.conn
        conn_string = "user='{user}' password='{pw}' dbname='{db}' host='{host}' port='{port}'".format(**self.connection_params)
        self.conn = psycopg2.connect(conn_string)
        return self.conn

    def close_connection(self):
        if self.conn:
            self.conn.close()

class DatabaseContext(PostgresConfig):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, connection_params):
        PostgresConfig.__init__(self, connection_params)