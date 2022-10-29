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

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self):
        table = super().get_table()
        custom_query = f"""
            SELECT * FROM {table} AS co
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
        custom_query = f"""
                    SELECT * FROM {table} AS co
                    INNER JOIN access_control.caixas AS c
                    ON c.id = co.id_caixa
                    INNER JOIN access_control.funcionarios AS f
                    ON f.cpf = co.cpf_operador
                    WHERE co.id = '{id_caixa_operador}'
                """

        row = super().get_by_pk('id', id_caixa_operador, custom_query)

        caixa_operador = None if row is None else CaixasOperadoresDAO.__parse_caixa_operador(row)
        return caixa_operador

    def get_caixa_opened_id(self, cpf_operador: str):
        table = super().get_table()
        custom_query = f"""
                            SELECT co .*, c .*, f .* FROM {table} AS co
                            INNER JOIN access_control.caixas AS c
                            ON c.id = co.id_caixa
                            INNER JOIN access_control.funcionarios AS f
                            ON f.cpf = co.cpf_operador
                            WHERE co.cpf_operador = '{cpf_operador}' AND c.aberto = 'true'
                        """

        row = super().get_by_pk('', 0, custom_query)

        caixa_operador = None if row is None else CaixasOperadoresDAO.__parse_caixa_operador(row)
        return caixa_operador

    def persist_entity(self, caixa_operador: CaixaOperador):
        table = super().get_table()
        columns = 'id, cpf_operador, id_caixa, data_horario_abertura, data_horario_fechamento, saldo_abertura, ' \
                  'saldo_fechamento, status, observacao, erros'

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                caixa_operador.id,
                caixa_operador.operador_caixa.cpf,
                caixa_operador.caixa.id,
                caixa_operador.data_horario_abertura,
                caixa_operador.data_horario_fechamento,
                caixa_operador.saldo_abertura,
                caixa_operador.saldo_fechamento,
                caixa_operador.status,
                caixa_operador.observacao,
                caixa_operador.erros,
            ),
        )

        return caixa_operador.id

    def delete_entity(self, id_caixa_operador: int):
        super().delete("id", id_caixa_operador)

    def update_entity(self, id_caixa_operador: int, attribute, value):
        super().update("id", id_caixa_operador, attribute, value)

    @staticmethod
    def __parse_caixa_operador(row):
        id = row['id']
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
        observacao = row['observacao']
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
            observacao,
            erros,
        )
