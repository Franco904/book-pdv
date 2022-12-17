from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.models.sangria import Sangria

class SangriasDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'sangrias')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        pass

    def get_all(self, custom_query=""):
        rows = super().get_all()
        sangrias = list(map(lambda row: SangriasDAO.parse_sangria(row), rows))
        return sangrias

    def get_all_by_caixa_operador(self, id_caixa_operador: int) -> []:
        rows = super().get_by_pk('id_caixa_operador', id_caixa_operador)

        return rows if rows is not None else []

    def get_by_id(self, id_sangria: int):
        row = super().get_by_pk("id", id_sangria)

        sangria = None if row is None else SangriasDAO.parse_sangria(row)
        return sangria

    def get_max_id(self) -> int:
        table = super().get_table()
        custom_query = f"""
                            SELECT MAX(co.id)
                            FROM {table} AS co
                        """

        row = super().get_by_pk('', 0, custom_query)

        return None if row is None else row[0]

    def persist_entity(self, sangria: Sangria) -> None:
        table = super().get_table()
        columns = "id_caixa_operador, data_horario, valor, observacao"

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s)""",
            (
                sangria.id_caixa_operador,
                sangria.data_horario,
                sangria.valor,
                sangria.observacao
            ),
        )

    @staticmethod
    def parse_sangria(row: dict) -> Sangria:
        id = row['id']
        id_caixa_operador = row['id_caixa_operador']
        data_horario = row['data_horario']
        valor = row['valor']
        observacao = row['observacao']

        return Sangria(id, id_caixa_operador, data_horario, valor, observacao)
