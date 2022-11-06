from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.models.caixa import Caixa
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.operador_caixa import OperadorCaixa


class CaixasOperadoresDAO(AbstractDAO):
    def __init__(self, database: Database):
        super().__init__(database, 'access_control', 'caixas_operadores')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    @staticmethod
    def __get_columns_joined():
        return ', '.join([
            'co.id AS caixa_operador_id', 'co.cpf_operador', 'co.id_caixa', 'co.data_horario_abertura', 'co.data_horario_fechamento',
            'co.saldo_abertura', 'co.saldo_fechamento', 'co.status', 'co.observacao_abertura', 'co.observacao_fechamento', 'co.erros',
            'c.id AS caixa_id', 'c.data_horario_criacao', 'c.saldo', 'c.aberto', 'c.ativo',
            'f.cpf', 'f.nome', 'f.telefone', 'f.senha', 'f.email', 'f.id_cargo',
        ])

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self):
        table = super().get_table()
        columns = CaixasOperadoresDAO.__get_columns_joined()

        custom_query = f"""
                            SELECT {columns} FROM {table} AS co
                            INNER JOIN access_control.caixas AS c
                            ON c.id = co.id_caixa
                            INNER JOIN access_control.funcionarios AS f
                            ON f.cpf = co.cpf_operador
                        """

        rows = super().get_all(custom_query)
        caixas_operadores = list(map(lambda row: CaixasOperadoresDAO.__parse_caixa_operador(row), rows))

        return caixas_operadores

    def get_by_id(self, id_caixa_operador: int):
        table = super().get_table()
        columns = CaixasOperadoresDAO.__get_columns_joined()

        custom_query = f"""
                            SELECT {columns} FROM {table} AS co
                            INNER JOIN access_control.caixas AS c
                            ON c.id = co.id_caixa
                            INNER JOIN access_control.funcionarios AS f
                            ON f.cpf = co.cpf_operador
                            WHERE co.id = '{id_caixa_operador}'
                        """

        row = super().get_by_pk('id', id_caixa_operador, custom_query)

        caixa_operador = None if row is None else CaixasOperadoresDAO.__parse_caixa_operador(row)
        return caixa_operador

    def get_caixa_opened_by_cpf(self, cpf_operador: str):
        table = super().get_table()
        columns = CaixasOperadoresDAO.__get_columns_joined()

        custom_query = f"""
                            SELECT {columns} FROM {table} AS co
                            INNER JOIN access_control.caixas AS c
                            ON c.id = co.id_caixa
                            INNER JOIN access_control.funcionarios AS f
                            ON f.cpf = co.cpf_operador
                            WHERE co.cpf_operador = '{cpf_operador}' AND c.aberto = 'true'
                        """

        row = super().get_by_pk('', 0, custom_query)

        caixa_operador = None if row is None else CaixasOperadoresDAO.__parse_caixa_operador(row)
        return caixa_operador

    def get_saldo_fechamento(self, id_caixa_operador: int, saldo_abertura: float) -> float:
        table = super().get_table()
        custom_query = f"""
                            SELECT SUM(v.valor_pago - v.valor_troco) AS vendas, SUM(s.valor) AS sangrias
                            FROM {table} AS co
                            INNER JOIN access_control.vendas AS v
                            ON v.id_caixa_operador = co.id
                            INNER JOIN access_control.sangrias AS s
                            ON s.id_caixa_operador = co.id
                            WHERE co.id = '{id_caixa_operador}'
                        """

        row = super().get_by_pk('', 0, custom_query)

        total_vendas = row['vendas'] if row['vendas'] is not None else 0
        total_sangrias = row['sangrias'] if row['sangrias'] is not None else 0

        saldo_fechamento = saldo_abertura + (total_vendas - total_sangrias)
        return saldo_fechamento

    def persist_entity(self, caixa_operador: CaixaOperador):
        table = super().get_table()
        columns = 'id, cpf_operador, id_caixa, data_horario_abertura, data_horario_fechamento, saldo_abertura, ' \
                  'saldo_fechamento, status, observacao_abertura, erros, observacao_fechamento'

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                caixa_operador.id,
                caixa_operador.operador_caixa.cpf,
                caixa_operador.caixa.id,
                caixa_operador.data_horario_abertura,
                caixa_operador.data_horario_fechamento,
                caixa_operador.saldo_abertura,
                caixa_operador.saldo_fechamento,
                caixa_operador.status,
                caixa_operador.observacao_abertura,
                caixa_operador.erros,
                caixa_operador.observacao_fechamento,
            ),
        )

        return caixa_operador.id

    def delete_entity(self, id_caixa_operador: int):
        super().delete("id", id_caixa_operador)

    def update_entity(self, id_caixa_operador: int, attribute, value):
        super().update("id", id_caixa_operador, attribute, value)

    @staticmethod
    def __parse_caixa_operador(row):
        id = row['caixa_operador_id']
        id_caixa = row['id_caixa']
        data_horario_criacao = row['data_horario_criacao']
        saldo = row['saldo']

        cpf_operador = row['cpf_operador']
        nome = row['nome']
        email = row["email"]
        telefone = row["telefone"]
        senha = row["senha"]

        data_horario_abertura = row['data_horario_abertura']
        data_horario_fechamento = row['data_horario_fechamento']
        saldo_abertura = row['saldo_abertura']
        saldo_fechamento = row['saldo_fechamento']
        status_caixa = row['status']
        observacao_abertura = row['observacao_abertura']
        observacao_fechamento = row['observacao_fechamento']
        erros = row['erros']

        return CaixaOperador(
            id,
            Caixa(
                id_caixa,
                data_horario_criacao,
                saldo
            ),
            OperadorCaixa(
                nome,
                cpf_operador,
                email,
                telefone,
                senha,
            ),
            data_horario_abertura,
            data_horario_fechamento,
            saldo_abertura,
            saldo_fechamento,
            status_caixa,
            observacao_abertura,
            observacao_fechamento,
            erros,
        )
