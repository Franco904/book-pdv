from src.data.dao.abstract_dao import AbstractDAO
from src.data.dao.produto_dao import ProdutoDAO
from src.data.database.database import Database
from src.domain.models.produto import Produto
from src.domain.models.venda_produtos import VendaProduto


class VendasProdutoDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'access_control', 'vendas_produtos')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    @staticmethod
    def __get_columns_joined():
        return ', '.join([
            'vp.id AS venda_produto_id', 'vp.id_venda', 'vp.id_produto', 'vp.quantidade',
            'p.id', 'p.id_tipo_produto', 'p.titulo', 'p.descricao', 'p.custo', 'p.margem_lucro',
            'p.fabricante',
            'p.autor', 'p.edicao', 'p.editora', 'p.isbn', 'p.pais', 'p.desconto'
        ])

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self, custom_query="") -> [VendaProduto]:
        table = super().get_table()
        columns = VendasProdutoDAO.__get_columns_joined()

        custom_query = f"""
                           SELECT {columns} FROM {table} vp
                           INNER JOIN access_control.produtos p
                           ON vp.id_produto = p.id
                        """

        rows = super().get_all(custom_query)

        venda_produtos = list(map(lambda row: VendasProdutoDAO.__parse_venda_produto(row), rows))

        return venda_produtos

    def get_by_id(self, id_venda_produto: int) -> VendaProduto | None:
        table = super().get_table()
        columns = VendasProdutoDAO.__get_columns_joined()

        custom_query = f"""
                           SELECT {columns} FROM {table} vp
                           INNER JOIN access_control.produtos p
                           ON vp.id_produto = p.id
                           WHERE venda_produto_id = {id_venda_produto}
                        """

        row = super().get_by_pk("id", id_venda_produto, custom_query)

        venda_produto = None if row is None else VendasProdutoDAO.__parse_venda_produto(row)
        return venda_produto

    def persist_entity(self, venda_produto: VendaProduto) -> None:
        table = super().get_table()
        columns = "id, id_venda, id_produto, quantidade"

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                venda_produto.id,
                venda_produto.id_venda,
                venda_produto.produto.id,
                venda_produto.quantidade
            ),
        )

    def delete_entity(self, id_venda_produto: int) -> None:
        super().delete("id", id_venda_produto)

    def update_entity(self, id_venda_produto: int, attribute, value) -> None:
        super().update("id", id_venda_produto, attribute, value)

    @staticmethod
    def __parse_venda_produto(row: dict):
        id = row['venda_produto_id']
        id_venda = row['id_venda']

        produto = ProdutoDAO.parse_produto(row)

        quantidade = row['quantidade']

        return VendaProduto(
            id,
            id_venda,
            produto,
            quantidade
        )
