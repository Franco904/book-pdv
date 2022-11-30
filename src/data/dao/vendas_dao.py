from datetime import datetime

from src.data.dao.abstract_dao import AbstractDAO
from src.data.dao.funcionario_dao import FuncionarioDAO
from src.data.dao.produto_dao import ProdutoDAO
from src.data.database.database import Database
from src.domain.enums import FiltroRelatorioVendasIntervaloEnum
from src.domain.models.venda import Venda
from src.domain.models.venda_produtos import VendaProduto


class VendasDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'access_control', 'vendas')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    @staticmethod
    def __get_columns_joined():
        return ', '.join([
            'v.id AS venda_id', 'v.id_caixa_operador', 'v.data_horario', 'v.valor_pago', 'v.valor_troco', 'v.observacao',
            'vp.id AS venda_produto_id', 'vp.id_venda', 'vp.id_produto', 'vp.quantidade',
            'p.id', 'p.id_tipo_produto', 'p.titulo', 'p.descricao', 'p.custo', 'p.margem_lucro',
            'p.fabricante',
            'p.autor', 'p.edicao', 'p.editora', 'p.isbn', 'p.pais', 'p.desconto',
            'f.cpf', 'f.nome', 'f.telefone', 'f.senha', 'f.email', 'f.id_cargo',
        ])

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all_with_products(self, id_caixa_operador=None) -> [Venda]:
        table = super().get_table()
        columns = VendasDAO.__get_columns_joined()

        custom_query = f"""
                           SELECT {columns} FROM {table} v
                           INNER JOIN access_control.vendas_produtos AS vp
                           ON v.id = vp.id_venda
                           INNER JOIN access_control.produtos AS p
                           ON p.id = vp.id_produto
                           INNER JOIN access_control.caixas_operadores AS co
                           ON v.id_caixa_operador = co.id
                           INNER JOIN access_control.funcionarios AS f
                           ON co.cpf_operador = f.cpf
                           {f'WHERE v.id_caixa_operador = {id_caixa_operador}' if id_caixa_operador is not None else ''}
                        """

        rows = super().get_all(custom_query)

        vendas = list(map(lambda row: VendasDAO.__parse_venda(row), rows))

        vendas_folded = []
        ff = [vendas_folded := VendasDAO.__fold_vendas(vendas_folded, v) for v in vendas]

        return vendas_folded

    def get_all_by_period_with_products(
            self,
            data_inicio=None,
            filtroIntervalo=FiltroRelatorioVendasIntervaloEnum.ultima_semana
    ) -> [Venda]:
        table = super().get_table()
        columns = VendasDAO.__get_columns_joined()
        data_inicio = datetime.now().strftime('%Y-%m-%d') if data_inicio is None else data_inicio

        custom_query = f"""
                           SELECT {columns} FROM {table} v
                           INNER JOIN access_control.vendas_produtos vp
                           ON v.id = vp.id_venda
                           INNER JOIN access_control.produtos p
                           ON p.id = vp.id_produto
                           INNER JOIN access_control.caixas_operadores AS co
                           ON v.id_caixa_operador = co.id
                           INNER JOIN access_control.funcionarios AS f
                           ON co.cpf_operador = f.cpf
                           WHERE v.data_horario::date <= '{data_inicio}'
                           AND v.data_horario::date >= '{data_inicio}'::date - INTERVAL {filtroIntervalo.value}
                        """

        rows = super().get_all(custom_query)

        vendas = list(map(lambda row: VendasDAO.__parse_venda(row), rows))

        vendas_folded = []
        ff = [vendas_folded := VendasDAO.__fold_vendas(vendas_folded, v) for v in vendas]

        return vendas_folded

    def get_operador_with_more_vendas_by_period(
            self,
            data_inicio=None,
            filtroIntervalo=FiltroRelatorioVendasIntervaloEnum.ultima_semana
    ) -> dict:
        table = super().get_table()
        data_inicio = datetime.now().strftime('%Y-%m-%d') if data_inicio is None else data_inicio

        custom_query = f"""
                            SELECT s.nome, s.total
                            FROM (
                                SELECT f.nome AS nome, SUM(v.valor_pago - v.valor_troco) AS total
                                FROM {table} AS v
                                INNER JOIN access_control.caixas_operadores AS co
                                ON v.id_caixa_operador = co.id
                                INNER JOIN access_control.funcionarios AS f
                                ON co.cpf_operador = f.cpf
                                WHERE v.data_horario::date <= '{data_inicio}'
                                AND v.data_horario::date >= '{data_inicio}'::date - INTERVAL {filtroIntervalo.value}
                                GROUP BY f.nome
                           ) AS s
                           ORDER BY s.total DESC
                           LIMIT 1;
                        """

        row = super().get_by_pk('', 0, custom_query)

        return {'nome': row[0], 'total': round(row[1], 2)} if row is not None else {'nome': '', 'total': ''}

    def get_by_id_with_products(self, id_venda: int) -> [Venda]:
        table = super().get_table()
        columns = VendasDAO.__get_columns_joined()

        custom_query = f"""
                           SELECT {columns} FROM {table} v
                           INNER JOIN access_control.vendas_produtos vp
                           ON v.id = vp.id_venda
                           INNER JOIN access_control.produtos p
                           ON p.id = vp.id_produto
                           INNER JOIN access_control.caixas_operadores AS co
                           ON v.id_caixa_operador = co.id
                           INNER JOIN access_control.funcionarios AS f
                           ON co.cpf_operador = f.cpf
                           WHERE v.id = {id_venda};
                        """

        rows = super().get_all(custom_query)

        vendas = list(map(lambda row: VendasDAO.__parse_venda(row), rows))

        venda_folded = None
        ff = [venda_folded := VendasDAO.__fold_into_single_venda(venda_folded, v) for v in vendas]

        return venda_folded

    def persist_entity(self, venda: Venda) -> None:
        table = super().get_table()
        columns = "id, id_caixa_operador, data_horario, valor_pago, valor_troco, observacao"

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                venda.id,
                venda.id_caixa_operador,
                venda.data_horario,
                venda.valor_pago,
                venda.valor_troco,
                venda.observacao,
            ),
        )

    def delete_entity(self, id_venda: int) -> None:
        super().delete("id", id_venda)

    def update_entity(self, id_venda: int, attribute, value) -> None:
        super().update("id", id_venda, attribute, value)

    @staticmethod
    def __parse_venda(row: dict) -> Venda | None:
        if row is None:
            return None

        id_venda = row['venda_id']
        id_caixa_operador = row['id_caixa_operador']
        data_horario = row['data_horario']
        valor_pago = row['valor_pago']
        valor_troco = row['valor_troco']
        observacao = row['observacao']

        id_venda_produto = row['venda_produto_id']
        quantidade = row['quantidade']
        produto = ProdutoDAO.parse_produto(row)

        funcionario = FuncionarioDAO.parse_funcionario(row)

        return Venda(
            id_venda,
            id_caixa_operador,
            funcionario,
            data_horario,
            valor_pago,
            valor_troco,
            observacao,
            [
                VendaProduto(
                    id_venda_produto,
                    id_venda,
                    produto,
                    quantidade,
                ),
            ]
        )

    @staticmethod
    def __fold_vendas(previous_vendas: [], current: Venda) -> [Venda]:
        """
            Reduz a coleção de vendas em uma coleção menor conforme um predicado

            Exemplo: Precisamos tratar o cenário de haver vários itens na lista de vendas com ids de venda repetidos,
            por conta de cada produto inserido dentro dela.

            -> Venda(1, [VendaProduto(1, Produto(5))])
            -> Venda(1, [VendaProduto(2, Produto(8))])
            Venda(2, [VendaProduto(3, Produto(5))])

            Resultado esperado após redução/fold:

            Venda(1, [VendaProduto(1, Produto(5)), VendaProduto(2, Produto(8))])
            Venda(2, [VendaProduto(3, Produto(5))])
        """
        if previous_vendas is None:
            return [].append(current)

        try:
            # Similar ao indexWhere((e) => e.id = current.id) da programação funcional
            index = next(i for i, venda in enumerate(previous_vendas) if venda.id == current.id)

            # Se encontrou índice, quer dizer que venda está repetida
            # Adiciona objeto venda-produto na lista de vendas-produtos da venda com mesmo id
            previous_vendas[index].venda_produtos.extend(current.venda_produtos)
        except StopIteration:
            # Se não encontrou índice, a venda de id novo é adicionada no final da lista
            previous_vendas.append(current)

        return previous_vendas

    @staticmethod
    def __fold_into_single_venda(previous_venda: Venda | None, current: Venda) -> [Venda]:
        """
            Reduz a coleção de vendas em um único objeto Venda conforme um predicado

            Exemplo:

            -> Venda(1, [VendaProduto(1, Produto(5))])
            -> Venda(1, [VendaProduto(2, Produto(8))])

            Resultado esperado após redução/fold:

            Venda(1, [VendaProduto(1, Produto(5)), VendaProduto(2, Produto(8))])
        """
        if previous_venda is None:
            return current

        if previous_venda.id == current.id:
            # Adiciona objeto venda-produto na lista de vendas-produtos da venda com mesmo id
            previous_venda.venda_produtos.extend(current.venda_produtos)

        return previous_venda
