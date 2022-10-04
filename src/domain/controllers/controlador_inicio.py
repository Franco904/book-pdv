import PySimpleGUI as sg

from src.domain.views.inicio.tela_inicio import TelaInicio


class ControladorInicio:
    def __init__(self, controlador_sistema) -> None:
        self.__tela_inicio = TelaInicio()
        self.__controlador_sistema = controlador_sistema

    def abre_historico(self):
        pass

    def abre_relatorios(self):
        pass

    def abre_produtos(self):
        pass

    def abre_funcionarios(self):
        self.__controlador_sistema.controllers["funcionarios"].abre_tela()

    def abre_caixa(self):
        self.__controlador_sistema.controllers["caixa"].abre_tela()

    def retornar(self):
        self.__tela_inicio.close()

    def abre_tela(self, isOperador = False):
        opcoesOperador = {
            1: self.abre_historico,
            2: self.retornar,
            3: self.abre_caixa,
        }

        opcoesSupervisor = {
            1: self.abre_relatorios,
            2: self.abre_produtos,
            3: self.abre_funcionarios,
            4: self.retornar,
        }

        while True:
            self.__tela_inicio.init_components(isOperador)

            opcao_escolhida = self.__tela_inicio.open()

            if opcao_escolhida in (0, None or sg.WIN_CLOSED):
                self.retornar()
                break
            elif isOperador:
                opcoesOperador[opcao_escolhida]()
            else:
                opcoesSupervisor[opcao_escolhida]()
