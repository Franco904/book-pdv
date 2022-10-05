from abc import ABC, abstractmethod
from src.data.database.database import Database
import pandas as pd
import sqlalchemy
import psycopg2

class AbstractDAO(ABC):

    @abstractmethod
    def __init__(self, database: Database, schema: str, table: str) -> None:
        self.__database = None
        self.__cache = {}
        self.__table = None
        self.__schema = None
        if isinstance(database, Database):
            self.__database = database
        if isinstance(table, str):
            self.__table = table
        if isinstance(schema, str):
            self.__schema = schema


    def read_all(self, schema, table):
        return pd.read_sql(f"SELECT * FROM {schema}.{table}")

    def truncate(self, schema, table):
        self.__database.open_connection().execute(f"TRUNCATE TABLE {schema}.{table}")

    def persist_all(self, schema, table):
        self.__database.open_connection().execute(f"INSERT INTO {schema}.{table} {self.__cache}")

    def execute_query(self, query: str):
        return pd.read_sql(query, self.__database.open_connection())

    #def remove_row(self, schema, table, row):
        #self.

    def get_all(self):
        return self.__cache.values()

    def get_all_keys(self):
        return self.__cache.keys()

    def persist_to_cache(self, key, obj):
        self.__cache[key] = obj
    def persist_row(self, schema, table):
        self.__database.open_connection().execute(f"INSERT INTO {schema}.{table} ")






