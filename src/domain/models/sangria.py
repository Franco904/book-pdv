
class Sangria:
    def __init__(self, id: int, id_caixa_operador: int, data_horario: str, valor: float | int, observacao: str):
        self.__id = None
        self.__id_caixa_operador = None
        self.__data_horario = None
        self.__valor = None
        self.__observacao = None

        if isinstance(id, int):
            self.__id = id
        if isinstance(id_caixa_operador, int):
            self.__id_caixa_operador = id_caixa_operador
        if isinstance(data_horario, str):
            self.__data_horario = data_horario
        if isinstance(valor, int) or isinstance(valor, float):
            self.__valor = valor
        if isinstance(observacao, str):
            self.__observacao = observacao

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
    def valor(self):
        return self.__valor

    @property
    def observacao(self):
        return self.__observacao
