from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.models.extrato_caixa import ExtratoCaixa


class ExtratoCaixaDAO(AbstractDAO):
    def __init__(self, database: Database):
        super().__init__(database, 'operador_caixa', 'extratos_caixa')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self, custom_query=''):
        rows = super().get_all()
        caixas = list(map(lambda row: ExtratoCaixaDAO.__parse_extrato_caixa(row), rows))

        return caixas

    def get_by_id(self, caixa_id: int):
        row = super().get_by_pk('id_caixa', caixa_id)

        caixa = None if row is None else ExtratoCaixaDAO.__parse_extrato_caixa(row)
        return caixa

    def persist_entity(self, extrato_caixa: ExtratoCaixa):
        table = super().get_table()
        columns = 'id_caixa, data_abertura, data_fechamento, saldo_abertura, saldo_fechamento, total_vendas, ' \
                  'total_sangrias, observacoes'

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                extrato_caixa.caixa.id,
                extrato_caixa.data_abertura,
                extrato_caixa.data_fechamento,
                extrato_caixa.saldo_abertura,
                extrato_caixa.saldo_fechamento,
                extrato_caixa.total_vendas,
                extrato_caixa.total_sangrias,
                extrato_caixa.observacoes,
            ),
        )

    def delete_entity(self, caixa_id: int):
        super().delete("id_caixa", caixa_id)

    def update_entity(self, caixa_id: int, attribute, value):
        super().update("id_caixa", caixa_id, attribute, value)

    @staticmethod
    def __parse_extrato_caixa(row):
        caixa_id = row["id_caixa"]
        data_abertura = row["data_abertura"]
        data_fechamento = row["data_fechamento"]
        saldo_abertura = row["saldo_abertura"]
        saldo_fechamento = row["saldo_fechamento"]
        total_vendas = row["total_vendas"]
        total_sangrias = row["total_sangrias"]
        observacoes = row["observacoes"]

        return ExtratoCaixa(
            caixa_id,
            data_abertura,
            saldo_abertura,
            observacoes,
            data_fechamento=data_fechamento,
            saldo_fechamento=saldo_fechamento,
            total_vendas=total_vendas,
            total_sangrias=total_sangrias,
        )
