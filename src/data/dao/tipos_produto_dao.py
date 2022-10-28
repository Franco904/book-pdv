from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.enums import TipoProdutoEnum


class TiposProdutoDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'access_control', 'tipos_produto')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def persist_entity(self, tipo_produto: TipoProdutoEnum) -> None:
        table = super().get_table()
        columns = "id, tipo_produto"

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s)""",
            (
                tipo_produto.value,
                tipo_produto.name,
            ),
        )

    def delete_entity(self, id: int) -> None:
        super().delete("id", id)

    def update_entity(self, id: int, attribute, value) -> None:
        super().update("id", id, attribute, value)

