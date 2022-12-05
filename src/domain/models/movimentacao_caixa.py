from datetime import datetime

from src.domain.enums import MovimentacaoCaixaEnum
from src.domain.models.operador_caixa import OperadorCaixa


class MovimentacaoCaixa:
    def __init__(self,
                 tipo: MovimentacaoCaixaEnum,
                 id: int,
                 data_horario: datetime,
                 movimentacao_total: float,
                 observacao: str,
                 operador: OperadorCaixa,
                 ):
        self.__tipo: None
        self.__id: None
        self.__data_horario = None
        self.__movimentacao_total = None
        self.__receita_total = None
        self.__observacao = None
        self.__operador = None

        if isinstance(tipo, MovimentacaoCaixaEnum):
            self.__tipo = tipo.value
        if isinstance(id, int):
            self.__id = id
        if isinstance(data_horario, datetime):
            self.__data_horario = data_horario
        if isinstance(movimentacao_total, float):
            self.__movimentacao_total = movimentacao_total
        if isinstance(observacao, str):
            self.__observacao = observacao
        if isinstance(operador, OperadorCaixa):
            self.__operador = operador

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def id(self) -> int:
        return self.__id

    @property
    def data_horario(self) -> datetime:
        return self.__data_horario

    @property
    def movimentacao_total(self) -> float:
        return self.__movimentacao_total

    @property
    def receita_total(self) -> float:
        return self.__receita_total

    @property
    def observacao(self) -> str:
        return self.__observacao

    @property
    def operador(self) -> OperadorCaixa:
        return self.__operador
