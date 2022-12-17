import psycopg2
from psycopg2.extras import DictCursor, DictConnection


class Database:
    def __init__(self):
        self.__hostname = "ec2-52-21-136-176.compute-1.amazonaws.com"
        self.__database = "d7uu5d256mpnp9"
        self.__username = "fsfxkuufatnhrp"
        self.__password = "b37a089e4e4128da0ac69de825da428c53862e0e0c67b26f276ef652b5519cc4"
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
    def connection(self) -> DictConnection:
        return self.__connection

    @property
    def cursor(self) -> DictCursor:
        return self.__cursor

    def close_all(self) -> None:
        self.close_cursor()
        self.close_connection()

    def close_connection(self) -> None:
        if self.__connection is not None:
            self.__connection.close()

    def close_cursor(self) -> None:
        if self.__cursor is not None:
            self.__cursor.close()
