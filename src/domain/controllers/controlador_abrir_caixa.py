import datetime

from src.domain.entities.caixa import Caixa
from src.domain.entities.extrato_caixa import ExtratoCaixa
from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.views.caixa.tela_abrir_caixa import TelaAbrirCaixa


class ControladorAbrirCaixa:
    def __init__(self, controlador_sistema) -> None:
        self.__tela_caixa = TelaAbrirCaixa()
        self.__controlador_sistema = controlador_sistema
        self.__caixas = None

        self.__data_abertura = datetime.datetime.now().strftime("%d/%m/%Y")
        self.load_caixas_fisicos()

    def load_caixas_fisicos(self):
        # Change this to get the data from DAO (Caixas)
        self.__caixas = [Caixa(1), Caixa(2), Caixa(3)]

    def abre_tela(self, operador_caixa: OperadorCaixa):
        caixas_disponiveis = list(
            filter(lambda caixa: caixa.operador_caixa is None or caixa.operador_caixa.cpf != operador_caixa.cpf,
                   self.__caixas)
        )
        caixas_ids = list(map(lambda caixa: caixa.id, caixas_disponiveis))

        self.__tela_caixa.init_components(caixas_ids, self.__data_abertura)
        result = self.__tela_caixa.open(caixas_disponiveis)

        if result["option"] == 0 or result["values"] is None:
            return self.retornar()

        result["values"]["saldo_abertura"] = result["saldo_abertura"]

        self.abrir_caixa(result["values"], operador_caixa)

    def abrir_caixa(self, values, operador_caixa: OperadorCaixa):
        if values is None:
            return

        filtered = list(filter(lambda caixa: caixa.id == values["caixa_id"], self.__caixas))
        if filtered is None:
            return

        caixa = filtered[0]

        # TODO: Gravar extrato no banco para posterior acesso no fechamento de caixa/relatórios
        caixa.operador_caixa = operador_caixa
        extrato = ExtratoCaixa(
            caixa,
            self.__data_abertura,
            values["saldo_abertura"],
            values["observacoes"]
        )

    def retornar(self):
        self.__tela_caixa.close()
        self.__controlador_sistema.controllers["inicio"].abre_tela(True)


