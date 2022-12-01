from datetime import datetime

from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.models.venda_produtos import VendaProduto


class Venda:
    def __init__(
            self,
            id: int,
            id_caixa_operador: int,
            operador: OperadorCaixa,
            data_horario: datetime,
            valor_pago: float,
            valor_troco: float,
            observacao: str,
            venda_produtos: [VendaProduto],
    ):
        self.__id = None
        self.__id_caixa_operador = None
        self.__operador = None
        self.__data_horario = None
        self.__valor_pago = None
        self.__valor_troco = 0
        self.__observacao = ''
        self.__venda_produtos = []

        if isinstance(id, int):
            self.__id = id
        if isinstance(id_caixa_operador, int):
            self.__id_caixa_operador = id_caixa_operador
        if isinstance(operador, OperadorCaixa):
            self.__operador = operador
        if isinstance(data_horario, datetime):
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
    def id(self) -> int:
        return self.__id

    @property
    def id_caixa_operador(self) -> int:
        return self.__id_caixa_operador

    @property
    def operador(self) -> OperadorCaixa:
        return self.__operador

    @property
    def data_horario(self) -> datetime:
        return self.__data_horario

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @property
    def valor_troco(self) -> float:
        return self.__valor_troco

    @property
    def observacao(self) -> str:
        return self.__observacao

    @property
    def venda_produtos(self) -> [VendaProduto]:
        return self.__venda_produtos

    def valor_total(self) -> float:
        return self.__valor_pago - self.__valor_troco
