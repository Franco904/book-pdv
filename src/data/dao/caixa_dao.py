from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.models.caixa import Caixa


class CaixaDAO(AbstractDAO):
    def __init__(self, database: Database):
        super().__init__(database, 'operador_caixa', 'caixas')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self):
        rows = super().get_all()
        caixas = list(map(lambda row: CaixaDAO.__parse_caixa(row), rows))

        return caixas

    def get_by_id(self, id: int):
        row = super().get_by_pk("id", id)

        caixa = None if row is None else CaixaDAO.__parse_caixa(row)
        return caixa

    def persist_entity(self, caixa: Caixa):
        table = super().get_table()
        columns = "id, cpf_operador, saldo"

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s)""",
            (
                caixa.id,
                caixa.operador_caixa.cpf,
                caixa.saldo,
            ),
        )

    def delete_entity(self, id: int):
        super().delete("id", id)

    def update_entity(self, id: int, attribute, value):
        super().update("id", id, attribute, value)

    @staticmethod
    def __parse_caixa(row):
        id = row["id"]
        cpf_operador = row["cpf_operador"]
        saldo = row["saldo"]

        return Caixa(id, cpf_operador, saldo, [], [])
