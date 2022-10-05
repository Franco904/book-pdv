from abc import ABC, abstractmethod

import psycopg2

from src.data.database.database import Database
import pandas as pd


class AbstractDAO(ABC):
    @abstractmethod
    def __init__(self, database: Database, schema: str, table: str) -> None:
        self.__database = None
        self.__table = None
        self.__schema = None
        if isinstance(database, Database):
            self.__database = database
        if isinstance(table, str):
            self.__table = table
        if isinstance(schema, str):
            self.__schema = schema
        self.__column_names = self.get_column_names()

    @property
    def schema(self):
        return self.__schema

    @property
    def table(self):
        return self.__table

    def get_table(self):
        return f"{self.__schema}.{self.__table}" if self.__schema is not None else f"{self.__table}"

    def get_column_names(self):
        if self.__table is not None:
            table = self.get_table()
            con, cursor = self.__database.connect()
            cursor.execute(f"SELECT * FROM {table} limit 0")
            return [desc[0] for desc in cursor.description]

    def execute_query(self, query: str):
        con, cursor = self.__database.connect()
        cursor.execute(query)
        rows = cursor.fetchall()
        self.__database.close_all()
        return rows

    def persist(self, query, records, many=False):
        try:
            con, cursor = self.__database.connect()
            if not many:
                cursor.execute(query, records)
            else:
                cursor.executemany(query, records)
            con.commit()
            print('Persistido.')
        except (Exception, psycopg2.Error) as error:
            print('Falha ao persistir.', error)
        finally:
            if con:
                self.__database.close_all()

    def get_all(self):
        table = f"{self.__schema}.{self.__table}" if self.__schema is not None else f"{self.__table}"
        con, cursor = self.__database.connect()
        cursor.execute(f"SELECT * FROM {table}")

        rows = cursor.fetchall()
        self.__database.close_all()
        return rows

    def delete(self, pk_name, target_pk):
        con, cursor = self.__database.connect()
        cursor.execute(f"DELETE FROM {self.get_table()} WHERE {pk_name} = '{target_pk}'")
        con.commit()
        self.__database.close_all()

    def get_by_pk(self, pk_name, target_pk):
        select_query = f"""SELECT * FROM {self.get_table()} WHERE {pk_name} = '{target_pk}'"""

        con, cursor = self.__database.connect()
        cursor.execute(select_query)

        row = cursor.fetchone()
        return row

    def update(self, pk_name, target_pk, attribute, value):
        if self.get_by_pk(pk_name, target_pk) is not None:
            con, cursor = self.__database.connect()
            cursor.execute(F"UPDATE {self.get_table()} SET {attribute} = {value} WHERE {pk_name} = '{target_pk}'")
            con.commit()
            self.__database.close_all()