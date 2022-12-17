from datetime import datetime

from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.enums import TipoProdutoEnum, FiltroRelatorioVendasIntervaloEnum
from src.domain.models.produto import Produto
from src.domain.models.livro import Livro
from src.domain.models.eletronico import Eletronico
from src.domain.models.produto_relatorio import ProdutoRelatorio


class ProdutoDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'produtos')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self, custom_query="") -> dict:
        rows = super().get_all()
        produtos = list(map(lambda row: ProdutoDAO.parse_produto(row), rows))
        livros = []
        eletronicos = []
        for produto in produtos:
            if produto.id_tipo_produto == 0:
                livros.append(produto)
            if produto.id_tipo_produto == 1:
                eletronicos.append(produto)
        return {'livros': livros, 'eletronicos': eletronicos}

    def has_product_venda(self, id_produto: int) -> bool:
        table = super().get_table()
        custom_query = f"""
                           SELECT id_venda FROM {table} p INNER JOIN book_pdv.vendas_produtos vp
                           ON p.id = vp.id_produto WHERE p.id = {id_produto}
                        """

        rows = super().get_all(custom_query)

        has_product_venda = False if len(rows) == 0 else True
        return has_product_venda

    def get_by_id(self, id_produto: int) -> Produto | None:
        row = super().get_by_pk("id", id_produto)

        produto = None if row is None else ProdutoDAO.parse_produto(row)
        return produto

    def get_most_sold_in_period(
            self,
            data_inicio=None,
            filtroIntervalo=FiltroRelatorioVendasIntervaloEnum.ultima_semana
    ) -> [ProdutoRelatorio]:
        table = super().get_table()
        data_inicio = datetime.now().strftime('%Y-%m-%d') if data_inicio is None else data_inicio

        custom_query = f"""
                            SELECT * FROM (
                                SELECT p.id, p.id_tipo_produto, p.titulo, p.descricao,
                                SUM(p.custo + (((p.margem_lucro - p.desconto) / 100) * p.custo)) AS receita_total,
                                SUM(vp.quantidade) AS quantidade
                                FROM {table} AS p
                                INNER JOIN book_pdv.vendas_produtos AS vp
                                ON p.id = vp.id_produto
                                INNER JOIN book_pdv.vendas AS v
                                ON v.id = vp.id_venda
                                WHERE v.data_horario::date <= '{data_inicio}'
                                AND v.data_horario::date >= '{data_inicio}'::date - INTERVAL {filtroIntervalo.value}
                                GROUP BY p.id, p.id_tipo_produto, p.titulo, p.descricao
                            ) AS s
                            ORDER BY s.quantidade DESC
                            LIMIT 5;
                        """

        rows = super().get_all(custom_query)
        produtos_relatorio = list(map(lambda row: ProdutoDAO.__parse_produto_relatorio(row), rows))

        return produtos_relatorio

    def persist_entity(self, produto: Produto) -> None:
        table = super().get_table()
        columns = "id, id_tipo_produto, titulo, descricao, custo, margem_lucro, fabricante, autor, edicao, editora, " \
                  "isbn, pais, desconto"

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                produto.id_produto,
                produto.id_tipo_produto,
                produto.titulo,
                produto.descricao,
                produto.custo,
                produto.margem_lucro,
                produto.fabricante,
                produto.autor,
                produto.edicao,
                produto.editora,
                produto.isbn,
                produto.pais,
                produto.desconto
            ),
        )

    def delete_entity(self, id_produto: int) -> None:
        super().delete("id", id_produto)

    def update_entity(self, id_produto: int, attribute, value) -> None:
        super().update("id", id_produto, attribute, value)

    @staticmethod
    def parse_produto(row: dict) -> Produto | None:
        if row is None:
            return None

        if row["id_tipo_produto"] == TipoProdutoEnum.livro.value:
            return ProdutoDAO.__parse_livro(row)

        elif row["id_tipo_produto"] == TipoProdutoEnum.eletronico.value:
            return ProdutoDAO.__parse_eletronico(row)

        else:
            raise Exception

    @staticmethod
    def __parse_livro(row: dict) -> Livro:
        id_produto = row['id']
        titulo = row['titulo']
        descricao = row['descricao']
        custo = row['custo']
        margem_lucro = row['margem_lucro']
        autor = row['autor']
        edicao = row['edicao']
        editora = row['editora']
        isbn = row['isbn']
        pais = row['pais']
        desconto = row['desconto']

        return Livro(id_produto,
                     titulo,
                     descricao,
                     custo,
                     margem_lucro,
                     autor,
                     edicao,
                     editora,
                     isbn,
                     pais,
                     desconto)

    @staticmethod
    def __parse_eletronico(row: dict) -> Eletronico:
        id_produto = row['id']
        titulo = row['titulo']
        descricao = row['descricao']
        custo = row['custo']
        margem_lucro = row['margem_lucro']
        fabricante = row['fabricante']
        desconto = row['desconto']

        return Eletronico(id_produto,
                          titulo,
                          descricao,
                          custo,
                          margem_lucro,
                          fabricante,
                          desconto)

    @staticmethod
    def __parse_produto_relatorio(row: dict) -> ProdutoRelatorio:
        id_produto = row['id']
        id_tipo_produto = row['id_tipo_produto']
        titulo = row['titulo']
        descricao = row['descricao']
        receita_total = row['receita_total']
        quantidade = row['quantidade']

        return ProdutoRelatorio(
            id_produto,
            id_tipo_produto,
            titulo,
            descricao,
            receita_total,
            quantidade,
        )
