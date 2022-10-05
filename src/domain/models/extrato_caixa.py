from src.domain.models.caixa import Caixa


class ExtratoCaixa:
    def __init__(self, caixa: Caixa, data_abertura: str, saldo_abertura: float, observacoes: str, data_fechamento=None, saldo_fechamento=None, total_vendas=None, total_sangrias=None):
        self.__caixa = None
        self.__data_abertura = None
        self.__data_fechamento = data_fechamento
        self.__saldo_abertura = None
        self.__saldo_fechamento = saldo_fechamento
        self.__total_vendas = total_vendas
        self.__total_sangrias = total_sangrias
        self.__observacoes = None

        if isinstance(caixa, Caixa):
            self.__caixa = caixa
        if isinstance(data_abertura, str):
            self.__data_abertura = data_abertura
        if isinstance(saldo_abertura, float):
            self.__saldo_abertura = saldo_abertura
        if isinstance(observacoes, str):
            self.__observacoes = observacoes

    @property
    def caixa(self):
        return self.__caixa

    @property
    def data_abertura(self):
        return self.__data_abertura

    @property
    def data_fechamento(self):
        return self.__data_fechamento

    @property
    def saldo_abertura(self):
        return self.__saldo_abertura

    @property
    def saldo_fechamento(self):
        return self.__saldo_fechamento

    @property
    def total_vendas(self):
        return self.__total_vendas

    @property
    def total_sangrias(self):
        return self.__total_sangrias

    @property
    def observacoes(self):
        return self.__observacoes

    @data_abertura.setter
    def data_abertura(self, data_abertura):
        if isinstance(data_abertura, str):
            self.__data_abertura = data_abertura

    @data_fechamento.setter
    def data_fechamento(self, data_fechamento):
        if isinstance(data_fechamento, str):
            self.__data_fechamento = data_fechamento

    @saldo_abertura.setter
    def saldo_abertura(self, saldo_abertura):
        if isinstance(saldo_abertura, float):
            self.__saldo_abertura = saldo_abertura

    @saldo_fechamento.setter
    def saldo_fechamento(self, saldo_fechamento):
        if isinstance(saldo_fechamento, float):
            self.__saldo_fechamento = saldo_fechamento

    @total_vendas.setter
    def total_vendas(self, total_vendas):
        if isinstance(total_vendas, float):
            self.__total_vendas = total_vendas

    @total_sangrias.setter
    def total_sangrias(self, total_sangrias):
        if isinstance(total_sangrias, float):
            self.__total_sangrias = total_sangrias

    @observacoes.setter
    def observacoes(self, observacoes):
        if isinstance(observacoes, str):
            self.__observacoes = observacoes
