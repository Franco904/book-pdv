from abc import ABC, abstractmethod

import psycopg2

from src.data.database.database import Database


class AbstractDAO(ABC):
    @abstractmethod
    def __init__(self, database: Database, table: str) -> None:
        self.__database = None
        self.__table = None
        self.__schema = "book_pdv"
        if isinstance(database, Database):
            self.__database = database
        if isinstance(table, str):
            self.__table = table
        self.__column_names = self.get_column_names()

    @property
    def schema(self) -> str:
        return self.__schema

    @property
    def table(self) -> str:
        return self.__table

    def get_table(self) -> str:
        return f"{self.__schema}.{self.__table}"

    def get_column_names(self) -> []:
        if self.__table is not None:
            table = self.get_table()
            con, cursor = self.__database.connect()
            cursor.execute(f"SELECT * FROM {table} limit 0")
            return [desc[0] for desc in cursor.description]

    def execute_query(self, query: str) -> []:
        con, cursor = self.__database.connect()
        cursor.execute(query)
        rows = cursor.fetchall()
        self.__database.close_all()
        return rows

    def persist(self, query, records, many=False, return_id=False) -> int | None:
        con, cursor = self.__database.connect()
        try:
            if not many:
                cursor.execute(query, records)
            else:
                cursor.executemany(query, records)
            con.commit()
            print('Persistido.')
        except (Exception, psycopg2.Error) as error:
            print('Falha ao persistir: ', error)
        finally:
            if con:
                id = None
                if return_id:
                    id = cursor.fetchone()[0]
                self.__database.close_all()
                return id

    def get_all(self, custom_query=None) -> []:
        con, cursor = self.__database.connect()

        select_query = custom_query if custom_query is not None else f"SELECT * FROM {self.get_table()}"
        cursor.execute(select_query)

        rows = cursor.fetchall()
        self.__database.close_all()
        return rows

    def delete(self, pk_name: str, target_pk: int) -> None:
        con, cursor = self.__database.connect()
        cursor.execute(f"DELETE FROM {self.get_table()} WHERE {pk_name} = '{target_pk}'")
        con.commit()
        self.__database.close_all()

    def delete_all(self) -> None:
        con, cursor = self.__database.connect()
        cursor.execute(f"DELETE FROM {self.get_table()}")
        con.commit()
        self.__database.close_all()

    def get_by_pk(self, pk_name: str, target_pk: int, custom_query=None) -> dict:
        select_query = custom_query if custom_query is not None else \
            f"SELECT * FROM {self.get_table()} WHERE {pk_name} = '{target_pk}' "

        con, cursor = self.__database.connect()
        cursor.execute(select_query)

        row = cursor.fetchone()
        return row

    def update(self, pk_name: str, target_pk: int, attribute: str, value) -> None:
        if self.get_by_pk(pk_name, target_pk) is not None:
            con, cursor = self.__database.connect()
            cursor.execute(F"UPDATE {self.get_table()} SET {attribute} = '{value}' WHERE {pk_name} = '{target_pk}'")
            con.commit()
            self.__database.close_all()
