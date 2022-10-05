from src.domain.models.operador_caixa import OperadorCaixa


class Caixa:
    def __init__(self, id, operador_caixa=None, saldo=0, vendas=None, sangrias=None):
        self.__id = None
        self.__operador_caixa = operador_caixa
        self.__saldo = None
        self.__vendas = vendas
        self.__sangrias = sangrias

        if isinstance(id, int):
            self.__id = id
        if isinstance(saldo, float):
            self.__saldo = saldo

    @property
    def id(self):
        return self.__id

    @property
    def operador_caixa(self):
        return self.__operador_caixa

    @property
    def saldo(self):
        return self.__saldo

    @property
    def vendas(self):
        return self.__vendas

    @property
    def sangrias(self):
        return self.__sangrias

    @operador_caixa.setter
    def operador_caixa(self, operador_caixa):
        if isinstance(operador_caixa, OperadorCaixa):
            self.__operador_caixa = operador_caixa

    @saldo.setter
    def saldo(self, saldo):
        if isinstance(saldo, float):
            self.__saldo = saldo

    @vendas.setter
    def vendas(self, vendas):
        if isinstance(vendas, list):
            self.__vendas = vendas

    @sangrias.setter
    def sangrias(self, sangrias):
        if isinstance(sangrias, list):
            self.__sangrias = sangrias
