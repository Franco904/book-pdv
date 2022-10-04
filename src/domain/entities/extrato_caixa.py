class ExtratoCaixa:
    def __init__(self, caixa, data_abertura, saldo_abertura, observacoes):
        self.__caixa = caixa
        self.__data_abertura = data_abertura
        self.__data_fechamento = None
        self.__saldo_abertura = saldo_abertura
        self.__saldo_fechamento = None
        self.__total_vendas = None
        self.__total_sangrias = None
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
        self.__data_abertura = data_abertura

    @data_fechamento.setter
    def data_fechamento(self, data_fechamento):
        self.__data_fechamento = data_fechamento

    @saldo_abertura.setter
    def saldo_abertura(self, saldo_abertura):
        self.__saldo_abertura = saldo_abertura

    @saldo_fechamento.setter
    def saldo_fechamento(self, saldo_fechamento):
        self.__saldo_fechamento = saldo_fechamento

    @total_vendas.setter
    def total_vendas(self, total_vendas):
        self.__total_vendas = total_vendas

    @total_sangrias.setter
    def total_sangrias(self, total_sangrias):
        self.__total_sangrias = total_sangrias

    @observacoes.setter
    def observacoes(self, observacoes):
        self.__observacoes = observacoes
