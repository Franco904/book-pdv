from abc import ABC, abstractmethod


class Produto(ABC):
    @abstractmethod
    def __init__(self,
                 id_tipo_produto: int,
                 titulo: str,
                 descricao: str,
                 custo: float | int,
                 margem_lucro: float | int,
                 fabricante: str,
                 autor: str,
                 edicao: str,
                 editora: str,
                 isbn: str,
                 pais: str,
                 desconto: float | int
                 ):
        self.__id_tipo_produto = None
        self.__titulo = None
        self.__descricao = None
        self.__custo = None
        self.__margem_lucro = None
        self.__fabricante = None
        self.__autor = None
        self.__edicao = None
        self.__editora = None
        self.__isbn = None
        self.__pais = None
        self.__desconto = None

        if isinstance(id_tipo_produto, int):
            self.__id_tipo_produto = id_tipo_produto
        if isinstance(titulo, str):
            self.__titulo = titulo
        if isinstance(descricao, str):
            self.__descricao = descricao
        if isinstance(custo, float):
            self.__custo = custo
        if isinstance(margem_lucro, float):
            self.__margem_lucro = margem_lucro
        if isinstance(fabricante, str):
            self.__fabricante = fabricante
        if isinstance(autor, str):
            self.__autor = autor
        if isinstance(edicao, str):
            self.__edicao = edicao
        if isinstance(editora, str):
            self.__editora = editora
        if isinstance(isbn, str):
            self.__isbn = isbn
        if isinstance(pais, str):
            self.__pais = pais
        if isinstance(desconto, float):
            self.__desconto = desconto

        self.__preco_final = self.calcula_preco_final()

    @property
    def id_tipo_produto(self) -> int:
        return self.__id_tipo_produto

    @id_tipo_produto.setter
    def id_tipo_produto(self, id_tipo_produto: int) -> None:
        if isinstance(id_tipo_produto, int):
            self.__id_tipo_produto = id_tipo_produto

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo: str) -> None:
        if isinstance(titulo, str):
            self.__titulo = titulo

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        if isinstance(descricao, str):
            self.__descricao = descricao

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float) -> None:
        if isinstance(custo, float):
            self.__custo = custo

    @property
    def margem_lucro(self) -> float:
        return self.__margem_lucro

    @margem_lucro.setter
    def margem_lucro(self, margem_lucro: float) -> None:
        if isinstance(margem_lucro, float):
            self.__margem_lucro = margem_lucro

    @property
    def fabricante(self) -> str:
        return self.__fabricante

    @fabricante.setter
    def fabricante(self, fabricante: str) -> None:
        if isinstance(fabricante, str):
            self.__fabricante = fabricante

    @property
    def autor(self) -> str:
        return self.__autor

    @autor.setter
    def autor(self, autor: str) -> None:
        if isinstance(autor, str):
            self.__autor = autor

    @property
    def edicao(self) -> str:
        return self.__edicao

    @edicao.setter
    def edicao(self, edicao: str) -> None:
        if isinstance(edicao, str):
            self.__edicao = edicao

    @property
    def editora(self) -> str:
        return self.__editora

    @editora.setter
    def editora(self, editora: str) -> None:
        if isinstance(editora, str):
            self.__editora = editora

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, isbn: str) -> None:
        if isinstance(isbn, str):
            self.__isbn = isbn

    @property
    def pais(self) -> str:
        return self.__pais

    @pais.setter
    def pais(self, pais: str) -> None:
        if isinstance(pais, str):
            self.__pais = pais

    @property
    def preco_final(self) -> float:
        return self.__preco_final

    def calcula_preco_final(self) -> int | float:
        margem_lucro_percentual_descontada = (self.margem_lucro - self.__desconto) / 100
        return self.__custo + (margem_lucro_percentual_descontada * self.__custo)

    def update_preco_final(self):
        self.__preco_final = self.calcula_preco_final()

    @property
    def desconto(self) -> float:
        return self.__desconto

    @desconto.setter
    def desconto(self, desconto: float) -> None:
        if isinstance(desconto, float):
            self.__desconto = desconto
