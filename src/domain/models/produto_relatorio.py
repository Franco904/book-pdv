class ProdutoRelatorio:
    def __init__(self,
                 id_produto: int,
                 id_tipo_produto: int,
                 titulo: str,
                 descricao: str,
                 receita_total: float,
                 quantidade: int,
                 ):
        self.__id_produto: None
        self.__id_tipo_produto: None
        self.__titulo = None
        self.__descricao = None
        self.__receita_total = None
        self.__quantidade = None

        if isinstance(id_produto, int):
            self.__id_produto = id_produto
        if isinstance(id_tipo_produto, int):
            self.__id_tipo_produto = id_tipo_produto
        if isinstance(titulo, str):
            self.__titulo = titulo
        if isinstance(descricao, str):
            self.__descricao = descricao
        if isinstance(receita_total, float):
            self.__receita_total = receita_total
        if isinstance(quantidade, int):
            self.__quantidade = quantidade

    @property
    def id_produto(self) -> int:
        return self.__id_produto

    @property
    def id_tipo_produto(self) -> int:
        return self.__id_tipo_produto

    @property
    def titulo(self) -> str:
        return self.__titulo

    @property
    def descricao(self) -> str:
        return self.__descricao

    @property
    def receita_total(self) -> float:
        return self.__receita_total

    @property
    def quantidade(self) -> int:
        return self.__quantidade
