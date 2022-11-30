from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.enums import MovimentacaoCaixaEnum
from src.domain.models.caixa import Caixa
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.movimentacao_caixa import MovimentacaoCaixa
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
            'co.id AS caixa_operador_id', 'co.cpf_operador', 'co.id_caixa', 'co.data_horario_abertura',
            'co.data_horario_fechamento',
            'co.saldo_abertura', 'co.saldo_fechamento', 'co.status', 'co.observacao_abertura',
            'co.observacao_fechamento', 'co.erros',
            'c.id AS caixa_id', 'c.data_horario_criacao', 'c.saldo', 'c.aberto', 'c.ativo',
            'f.cpf', 'f.nome', 'f.telefone', 'f.senha', 'f.email',
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

    def get_all_by_caixa_id(self, id_caixa: int):
        table = super().get_table()
        columns = CaixasOperadoresDAO.__get_columns_joined()

        custom_query = f"""
                            SELECT {columns} FROM {table} AS co
                            INNER JOIN access_control.caixas AS c
                            ON c.id = co.id_caixa
                            INNER JOIN access_control.funcionarios AS f
                            ON f.cpf = co.cpf_operador
                            WHERE co.id_caixa = '{id_caixa}'
                        """

        rows = super().get_all(custom_query)
        caixas_operadores = list(map(lambda row: CaixasOperadoresDAO.__parse_caixa_operador(row), rows))

        return caixas_operadores

    def get_all_by_caixa_id_and_cpf(self, id_caixa: int, cpf_operador: str | None):
        table = super().get_table()
        columns = CaixasOperadoresDAO.__get_columns_joined()

        custom_query = f"""
                            SELECT {columns} FROM {table} AS co
                            INNER JOIN access_control.caixas AS c
                            ON c.id = co.id_caixa
                            INNER JOIN access_control.funcionarios AS f
                            ON f.cpf = co.cpf_operador
                            WHERE co.id_caixa = '{id_caixa}'
                            {f"AND co.cpf_operador = '{cpf_operador}'" if cpf_operador is not None else ''}
                        """

        rows = super().get_all(custom_query)
        caixas_operadores = list(map(lambda row: CaixasOperadoresDAO.__parse_caixa_operador(row), rows))

        return caixas_operadores

    def get_movimentacoes_by_caixa_id(self, id_caixa: int):
        table = super().get_table()

        custom_query_vendas = f"""
                                    SELECT v.id, v.data_horario, SUM(v.valor_pago - v.valor_troco) AS total_movimentado,
                                    v.observacao, f.cpf, f.nome, f.telefone, f.senha, f.email
                                    FROM {table} AS co
                                    INNER JOIN access_control.caixas AS c
                                    ON c.id = co.id_caixa
                                    INNER JOIN access_control.funcionarios AS f
                                    ON f.cpf = co.cpf_operador
                                    INNER JOIN access_control.vendas AS v
                                    ON v.id_caixa_operador = co.id
                                    WHERE co.id_caixa = '{id_caixa}'
                                    GROUP BY v.id, v.data_horario, v.observacao, f.cpf, f.nome, f.telefone, f.senha, f.email
                                    ORDER BY v.data_horario DESC;
                                """

        custom_query_sangrias = f"""
                                    SELECT s.id, s.data_horario, SUM(s.valor) AS total_movimentado,
                                    s.observacao, f.cpf, f.nome, f.telefone, f.senha, f.email
                                    FROM {table} AS co
                                    INNER JOIN access_control.caixas AS c
                                    ON c.id = co.id_caixa
                                    INNER JOIN access_control.funcionarios AS f
                                    ON f.cpf = co.cpf_operador
                                    INNER JOIN access_control.sangrias AS s
                                    ON s.id_caixa_operador = co.id
                                    WHERE co.id_caixa = '{id_caixa}'
                                    GROUP BY s.id, s.data_horario, s.observacao, f.cpf, f.nome, f.telefone, f.senha, f.email
                                    ORDER BY s.data_horario DESC;
                                """

        rows_vendas = super().get_all(custom_query_vendas)
        rows_sangrias = super().get_all(custom_query_sangrias)

        movimentacoes = [
            CaixasOperadoresDAO.__parse_movimentacao_caixa(row_venda, MovimentacaoCaixaEnum.venda)
            for row_venda in rows_vendas
        ]

        movimentacoes.extend([
            CaixasOperadoresDAO.__parse_movimentacao_caixa(row_sangria, MovimentacaoCaixaEnum.sangria)
            for row_sangria in rows_sangrias
        ])

        return movimentacoes

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
        custom_query_vendas = f"""
                                    SELECT SUM(v.valor_pago - v.valor_troco)
                                    FROM {table} AS co
                                    LEFT OUTER JOIN access_control.vendas AS v
                                    ON v.id_caixa_operador = co.id
                                    GROUP BY co.id
                                    HAVING co.id = '{id_caixa_operador}'
                              """

        custom_query_sangrias = f"""
                                    SELECT SUM(s.valor)
                                    FROM {table} AS co
                                    LEFT OUTER JOIN access_control.sangrias AS s
                                    ON s.id_caixa_operador = co.id
                                    GROUP BY co.id
                                    HAVING co.id = '{id_caixa_operador}'
                              """

        row_vendas = super().get_by_pk('', 0, custom_query_vendas)
        row_sangrias = super().get_by_pk('', 0, custom_query_sangrias)

        total_vendas = row_vendas[0] if row_vendas[0] is not None else 0
        total_sangrias = row_sangrias[0] if row_sangrias[0] is not None else 0

        saldo_fechamento = saldo_abertura + (total_vendas - total_sangrias)
        return saldo_fechamento

    def get_max_id(self) -> int:
        table = super().get_table()
        custom_query = f"""
                            SELECT MAX(co.id)
                            FROM {table} AS co
                        """

        row = super().get_by_pk('', 0, custom_query)

        return None if row is None else row[0]

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

    @staticmethod
    def __parse_movimentacao_caixa(row, tipo: MovimentacaoCaixaEnum):
        id_movimentacao = row['id']
        data_horario = row['data_horario']
        total_movimentado = row['total_movimentado']
        observacao = row['observacao']

        cpf_operador = row['cpf']
        nome = row['nome']
        email = row['email']
        telefone = row['telefone']
        senha = row['senha']

        return MovimentacaoCaixa(
            tipo,
            id_movimentacao,
            data_horario,
            total_movimentado,
            observacao,
            OperadorCaixa(
                nome,
                cpf_operador,
                email,
                telefone,
                senha,
            ),
        )
