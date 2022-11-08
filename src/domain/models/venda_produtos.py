from src.domain.models.produto import Produto


class VendaProduto:
    def __init__(
            self,
            id: int,
            id_venda: int,
            produto: Produto,
            quantidade: int,
    ):
        self.__id = None
        self.__id_venda = None
        self.__produto = None
        self.__quantidade = None

        if isinstance(id, int):
            self.__id = id
        if isinstance(id_venda, int):
            self.__id_venda = id_venda
        if isinstance(produto, Produto):
            self.__produto = produto
        if isinstance(quantidade, int):
            self.__quantidade = quantidade

    @property
    def id(self):
        return self.__id

    @property
    def id_venda(self):
        return self.__id_venda

    @property
    def produto(self):
        return self.__produto

    @property
    def quantidade(self):
        return self.__quantidade
