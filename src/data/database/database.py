import psycopg2
from psycopg2.extras import DictCursor


class Database:
    def __init__(self):
        self.__hostname = "54.147.36.107"
        self.__database = "dfb5983k0abcf8"
        self.__username = "rusdkrqlyrnzgx"
        self.__password = "a7b9f182a0e99bf63b4f19c63eee7db3aa5691840897684266ee56796e9d74f8"
        self.__port = 5432
        self.__connection = None
        self.__cursor = None

    def connect(self):
        self.__connection = psycopg2.connect(
            host=self.__hostname,
            database=self.__database,
            user=self.__username,
            password=self.__password,
            port=self.__port,
            cursor_factory=DictCursor
        )
        self.__cursor = self.__connection.cursor()

        return [self.__connection, self.cursor]

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor

    def close_all(self):
        self.close_cursor()
        self.close_connection()

    def close_connection(self):
        if self.__connection is not None:
            self.__connection.close()

    def close_cursor(self):
        if self.__cursor is not None:
            self.__cursor.close()
