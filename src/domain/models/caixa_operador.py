import datetime

from src.domain.enums import StatusCaixaAberto
from src.domain.models.caixa import Caixa
from src.domain.models.operador_caixa import OperadorCaixa


class CaixaOperador:
    def __init__(
            self,
            id: int,
            caixa: Caixa,
            operador_caixa: OperadorCaixa,
            data_horario_abertura: datetime,
            data_horario_fechamento: datetime,
            saldo_abertura: float,
            saldo_fechamento: float,
            status: StatusCaixaAberto,
            observacao: str,
            erros: str,
    ):
        self.__id = None
        self.__caixa = None
        self.__operador_caixa = None
        self.__data_horario_abertura = None
        self.__data_horario_fechamento = None
        self.__saldo_abertura = None
        self.__saldo_fechamento = None
        self.__status = StatusCaixaAberto.positivo.name
        self.__observacao = None
        self.__erros = None

        if isinstance(id, int):
            self.__id = id
        if isinstance(operador_caixa, OperadorCaixa):
            self.__operador_caixa = operador_caixa
        if isinstance(caixa, Caixa):
            self.__caixa = caixa
        if isinstance(data_horario_abertura, datetime.datetime):
            self.__data_horario_abertura = data_horario_abertura
        if isinstance(data_horario_fechamento, datetime.datetime):
            self.__data_horario_fechamento = data_horario_fechamento
        if isinstance(saldo_abertura, float):
            self.__saldo_abertura = saldo_abertura
        if isinstance(saldo_fechamento, float):
            self.__saldo_fechamento = saldo_fechamento
        if isinstance(status, StatusCaixaAberto):
            self.__status = status.name
        if isinstance(observacao, str):
            self.__observacao = observacao
        if isinstance(erros, str):
            self.__erros = erros

    @property
    def id(self):
        return self.__id

    @property
    def caixa(self):
        return self.__caixa

    @caixa.setter
    def caixa(self, caixa):
        if isinstance(caixa, Caixa):
            self.__caixa = caixa

    @property
    def operador_caixa(self):
        return self.__operador_caixa

    @operador_caixa.setter
    def operador_caixa(self, operador_caixa):
        if isinstance(operador_caixa, OperadorCaixa):
            self.__operador_caixa = operador_caixa

    @property
    def data_horario_abertura(self):
        return self.__data_horario_abertura

    @data_horario_abertura.setter
    def data_horario_abertura(self, data_horario_abertura):
        if isinstance(data_horario_abertura, datetime.datetime):
            self.__data_horario_abertura = data_horario_abertura

    @property
    def data_horario_fechamento(self):
        return self.__data_horario_fechamento

    @data_horario_fechamento.setter
    def data_horario_fechamento(self, data_horario_fechamento):
        if isinstance(data_horario_fechamento, datetime.datetime):
            self.__data_horario_fechamento = data_horario_fechamento

    @property
    def saldo_abertura(self):
        return self.__saldo_abertura

    @saldo_abertura.setter
    def saldo_abertura(self, saldo_abertura):
        if isinstance(saldo_abertura, float):
            self.__saldo_abertura = saldo_abertura

    @property
    def saldo_fechamento(self):
        return self.__saldo_fechamento

    @saldo_fechamento.setter
    def saldo_fechamento(self, saldo_fechamento):
        if isinstance(saldo_fechamento, float):
            self.__saldo_fechamento = saldo_fechamento

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        if isinstance(status, StatusCaixaAberto):
            self.__status = status

    @property
    def observacao(self):
        return self.__observacao

    @observacao.setter
    def observacao(self, observacao):
        if isinstance(observacao, str):
            self.__observacao = observacao

    @property
    def erros(self):
        return self.__erros

    @erros.setter
    def erros(self, erros):
        if isinstance(erros, str):
            self.__erros = erros
