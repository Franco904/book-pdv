from src.domain.entities.caixa import Caixa
from src.domain.entities.extrato_caixa import ExtratoCaixa
from src.domain.views.caixa.tela_abrir_caixa import TelaAbrirCaixa


class ControladorAbrirCaixa:
    def __init__(self, controlador_sistema) -> None:
        self.__tela_caixa = TelaAbrirCaixa()
        self.__controlador_sistema = controlador_sistema
        self.__caixas_fisicos = None

        self.load_caixas_fisicos()

    def load_caixas_fisicos(self):
        # Change this to get the data from DAO (Caixas)
        self.__caixas_fisicos = [
            Caixa(1, 'Caixa 1'),
            Caixa(2, 'Caixa 2'),
            Caixa(3, 'Caixa 3'),
        ]

    def abrir_caixa(self, values):
        if values is None:
            return

        filtered = list(filter(lambda caixa: caixa.nome == values["nome_caixa"], self.__caixas_fisicos))
        if filtered is None:
            return

        caixa = filtered[0]
        extrato = ExtratoCaixa(
            caixa.id,
            values["data_abertura"],
            values["saldo_abertura"],
            values["observacoes"]
        )

        # TODO: Gravar extrato no banco para posterior acesso no fechamento de caixa/relatórios

    def retornar(self):
        self.__tela_caixa.close()
        self.__controlador_sistema.controllers["inicio"].abre_tela(True)

    def abre_tela(self):
        caixas_names = list(map(lambda caixa: caixa.nome, self.__caixas_fisicos))
        self.__tela_caixa.init_components(caixas_names)

        option, values = self.__tela_caixa.open()

        if option == 0:
            return self.retornar()

        self.abrir_caixa(values)
