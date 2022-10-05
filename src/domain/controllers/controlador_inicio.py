import PySimpleGUI as sg

from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.views.inicio.tela_inicio import TelaInicio


class ControladorInicio:
    def __init__(self, controlador_sistema) -> None:
        self.__tela_inicio = TelaInicio()
        self.__controlador_sistema = controlador_sistema
        self.__funcionario = None

    def abre_historico(self):
        pass

    def abre_relatorios(self):
        pass

    def abre_produtos(self):
        pass

    def abre_funcionarios(self):
        self.__controlador_sistema.controllers["funcionarios"].abre_tela()

    def abre_caixa(self):
        self.__controlador_sistema.controllers["caixa"].abre_tela(self.__funcionario)

    def retornar(self):
        self.__tela_inicio.close()

    def abre_tela(self, is_operador = False):
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
            self.__tela_inicio.init_components(is_operador)

            opcao_escolhida = self.__tela_inicio.open()

            if opcao_escolhida in (0, None or sg.WIN_CLOSED):
                self.retornar()
                break
            elif is_operador:
                self.__funcionario = OperadorCaixa("Franco", "12833158904", "teste@gmail", "991300904", "123123as")
                opcoesOperador[opcao_escolhida]()
            else:
                opcoesSupervisor[opcao_escolhida]()
