class Caixa:
    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome
        self.__saldo = 0
        self.__vendas = 0
        self.__sangrias = 0

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def saldo(self):
        return self.__saldo

    @property
    def vendas(self):
        return self.__vendas

    @property
    def sangrias(self):
        return self.__sangrias

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @saldo.setter
    def saldo(self, saldo):
        self.__saldo = saldo

    @vendas.setter
    def vendas(self, vendas):
        self.__vendas = vendas

    @sangrias.setter
    def sangrias(self, sangrias):
        self.__sangrias = sangrias
