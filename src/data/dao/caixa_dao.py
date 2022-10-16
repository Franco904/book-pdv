from src.data.dao.abstract_dao import AbstractDAO
from src.data.dao.funcionario_dao import FuncionarioDAO
from src.data.database.database import Database
from src.domain.models.caixa import Caixa
from src.domain.models.funcionario import Funcionario


class CaixaDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'operador_caixa', 'caixas')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self, custom_query=" WHERE cpf_operador = ''") -> [Caixa]:
        rows = super().get_all(custom_query)
        caixas = list(map(lambda row: self.__parse_caixa(row), rows))

        return caixas

    def get_by_id(self, id: int) -> Caixa | None:
        row = super().get_by_pk("id", id)

        caixa = None if row is None else self.__parse_caixa(row)
        return caixa

    def persist_entity(self, caixa: Caixa) -> None:
        table = super().get_table()
        columns = "id_caixa, cpf_operador, saldo"

        caixa_cpf = "" if caixa.operador_caixa is None else caixa.operador_caixa.cpf

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s)""",
            (
                caixa.id,
                caixa_cpf,
                caixa.saldo,
            ),
        )

    def delete_entity(self, id: int) -> None:
        super().delete("id_caixa", id)

    def update_entity(self, id: int, attribute, value) -> None:
        super().update("id_caixa", id, attribute, value)

    def __parse_caixa(self, row) -> Caixa:
        id = row["id_caixa"]
        cpf_operador = row["cpf_operador"]
        saldo = row["saldo"]

        operador_caixa: Funcionario = FuncionarioDAO(self.__database).get_by_cpf(cpf_operador)

        return Caixa(id, operador_caixa, saldo, [], [])
