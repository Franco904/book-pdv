import datetime

from src.domain.models.venda_produtos import VendaProduto


class Venda:
    def __init__(
            self,
            id: int,
            id_caixa_operador: int,
            data_horario: datetime,
            valor_pago: float,
            valor_troco: float,
            observacao: str,
            venda_produtos: [VendaProduto],
    ):
        self.__id = None
        self.__caixa_operador = None
        self.__data_horario = None
        self.__valor_pago = None
        self.__valor_troco = 0
        self.__observacao = ''
        self.__venda_produtos = []

        if isinstance(id, int):
            self.__id = id
        if isinstance(id_caixa_operador, int):
            self.__id_caixa_operador = int
        if isinstance(data_horario, datetime.datetime):
            self.__data_horario = data_horario
        if isinstance(valor_pago, float):
            self.__valor_pago = valor_pago
        if isinstance(valor_troco, float):
            self.__valor_troco = valor_troco
        if isinstance(observacao, str):
            self.__observacao = observacao
        if isinstance(venda_produtos, list):
            self.__venda_produtos = venda_produtos

    @property
    def id(self):
        return self.__id

    @property
    def id_caixa_operador(self):
        return self.__id_caixa_operador

    @property
    def data_horario(self):
        return self.__data_horario

    @property
    def valor_pago(self):
        return self.__valor_pago

    @property
    def valor_troco(self):
        return self.__valor_troco

    @property
    def observacao(self):
        return self.__observacao

    @property
    def venda_produtos(self):
        return self.__venda_produtos

    def valor_total(self):
        return self.__valor_pago - self.__valor_troco
