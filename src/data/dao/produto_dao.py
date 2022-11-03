from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.enums import TipoProdutoEnum
from src.domain.models.produto import Produto
from src.domain.models.livro import Livro
from src.domain.models.eletronico import Eletronico


class ProdutoDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'access_control', 'produtos')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self, custom_query="") -> [Produto]:
        rows = super().get_all()
        produtos = list(map(lambda row: ProdutoDAO.__parse_produto(row), rows))
        livros = []
        eletronicos = []
        for produto in produtos:
            if produto.id_tipo_produto == 0:
                livros.append(produto)
            if produto.id_tipo_produto == 1:
                eletronicos.append(produto)
        return {'livros': livros, 'eletronicos': eletronicos}

    def get_by_id(self, id_produto: int) -> Produto | None:
        row = super().get_by_pk("id", id_produto)

        produto = None if row is None else ProdutoDAO.__parse_produto(row)
        return produto

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
    def __parse_produto(row) -> Produto | None:
        if row is None:
            return None

        if row["id_tipo_produto"] == TipoProdutoEnum.livro.value:
            return ProdutoDAO.__parse_livro(row)

        elif row["id_cargo"] == TipoProdutoEnum.eletronico.value:
            return ProdutoDAO.__parse_eletronico(row)

        else:
            raise Exception

    @staticmethod
    def __parse_livro(row) -> Livro:
        id_produto = row['id_produto']
        id_tipo_produto = row['id_tipo_produto']
        titulo = row['produto.titulo']
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
                     id_tipo_produto,
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
    def __parse_eletronico(row) -> Eletronico:
        id_produto = row['id_produto']
        id_tipo_produto = row['id_tipo_produto']
        titulo = row['produto.titulo']
        descricao = row['descricao']
        custo = row['custo']
        margem_lucro = row['margem_lucro']
        fabricante = row['fabricante']
        desconto = row['desconto']

        return Eletronico(id_produto,
                          id_tipo_produto,
                          titulo,
                          descricao,
                          custo,
                          margem_lucro,
                          fabricante,
                          desconto)
