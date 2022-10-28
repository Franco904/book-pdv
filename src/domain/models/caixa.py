import datetime


class Caixa:
    def __init__(self, id, data_horario_criacao=None, saldo=0.0):
        self.__id = None
        self.__data_horario_criacao = datetime.datetime.now()
        self.__saldo = None

        if isinstance(id, int):
            self.__id = id
        if isinstance(data_horario_criacao, datetime.datetime):
            self.__data_horario_criacao = data_horario_criacao
        if isinstance(saldo, float):
            self.__saldo = saldo

    @property
    def id(self):
        return self.__id

    @property
    def data_horario_criacao(self):
        return self.__data_horario_criacao

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo):
        if isinstance(saldo, float):
            self.__saldo = saldo
