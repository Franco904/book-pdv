from src.domain.entities.tables.caixa_fisico import CaixaFisico
from src.domain.views.caixa.tela_abrir_caixa import TelaAbrirCaixa


class ControladorAbrirCaixa:
    def __init__(self, controlador_sistema) -> None:
        self.__tela_caixa = TelaAbrirCaixa()
        self.__controlador_sistema = controlador_sistema
        self.__caixas_fisicos = None

        self.loadCaixasFisicos()

    def loadCaixasFisicos(self):
        # Change this to get the data from DAO (Caixas)
        self.__caixas_fisicos = [
            CaixaFisico(1, 'Caixa 1'),
            CaixaFisico(2, 'Caixa 2'),
            CaixaFisico(3, 'Caixa 3'),
        ]

    def abrir_caixa(self, values):
        print(values)

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
