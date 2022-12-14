from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.models.caixa import Caixa


class CaixaDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'caixas')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self) -> [Caixa]:
        rows = super().get_all()
        caixas = list(map(lambda row: CaixaDAO.__parse_caixa(row), rows))

        return caixas

    def get_all_to_open(self) -> [Caixa]:
        table = super().get_table()
        custom_query = f"SELECT * FROM {table} WHERE aberto = '0' AND ativo = '1'"

        rows = super().get_all(custom_query)
        caixas = list(map(lambda row: CaixaDAO.__parse_caixa(row), rows))

        return caixas

    def get_by_id(self, id: int) -> Caixa | None:
        row = super().get_by_pk("id", id)

        caixa = None if row is None else CaixaDAO.__parse_caixa(row)
        return caixa

    def get_ativo_by_id(self, id: int) -> Caixa | None:
        table = super().get_table()
        custom_query = f"SELECT * FROM {table} WHERE id = '{id}' AND ativo = '1'"

        row = super().get_by_pk('', 0, custom_query)

        caixa = None if row is None else CaixaDAO.__parse_caixa(row)
        return caixa

    def persist_entity(self, caixa: Caixa) -> None:
        table = super().get_table()
        columns = "id, data_horario_criacao, saldo, aberto, ativo"

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s)""",
            (
                caixa.id,
                caixa.data_horario_criacao,
                caixa.saldo,
                0,
                1,
            ),
        )

    def open_caixa(self, id: int):
        super().update("id", id, 'aberto', 1)

    def close_caixa(self, id: int):
        super().update("id", id, 'aberto', 0)

    def inactivate_entity(self, id: int):
        super().update("id", id, 'ativo', 0)

    def delete_entity(self, id: int) -> None:
        super().delete("id", id)

    def update_entity(self, id: int, attribute, value) -> None:
        super().update("id", id, attribute, value)

    @staticmethod
    def __parse_caixa(row) -> Caixa:
        id = row["id"]
        data_horario_criacao = row["data_horario_criacao"]
        saldo = row["saldo"]

        return Caixa(id, data_horario_criacao, saldo)
