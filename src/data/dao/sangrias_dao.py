from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.enums import CargoEnum


class SangriasDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'access_control', 'sangrias')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        pass

    def get_all(self, custom_query=""):
        pass

    def get_all_by_caixa_operador(self, id_caixa_operador: int) -> []:
        rows = super().get_by_pk('id_caixa_operador', id_caixa_operador)

        return rows if rows is not None else []

    def get_by_id(self, id: int):
        pass

    def persist_entity(self, cargo: CargoEnum) -> None:
        pass

    def delete_entity(self, id: int) -> None:
        pass

    def update_entity(self, id: int, attribute, value) -> None:
        pass

