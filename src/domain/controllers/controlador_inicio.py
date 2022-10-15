import PySimpleGUI as sg

from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.views.inicio.tela_inicio import TelaInicio
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorInicio:
    def __init__(self, controlador_sistema) -> None:
        self.__tela_inicio = TelaInicio()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__controlador_sistema = controlador_sistema
        self.__funcionario = None

    def abre_caixas_abertos(self):
        # Visualização dos dados dos caixas que foram abertos
        pass

    def abre_relatorios(self):
        # Visualização dos dados das vendas registradas
        pass

    def abre_produtos(self):
        # Visualização dos dados dos produtos registrados
        pass

    def abre_funcionarios(self):
        self.__controlador_sistema.controllers["funcionarios"].abre_tela()

    def abre_caixa(self):
        self.__controlador_sistema.controllers["abrir_caixa"].abre_tela(self.__funcionario)

    def retornar(self):
        self.__tela_inicio.close()
        exit(0)

    def abre_tela(self, is_operador=True):
        opcoes_operador = {
            1: self.abre_caixas_abertos,
            2: self.retornar,
            3: self.abre_caixa,
        }

        opcoes_supervisor = {
            1: self.abre_relatorios,
            2: self.abre_produtos,
            3: self.abre_funcionarios,
            4: self.retornar,
        }

        while True:
            self.__tela_inicio.init_components(is_operador)

            opcao_escolhida = self.__tela_inicio.open()

            if opcao_escolhida in (0, None, sg.WIN_CLOSED):
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()
                self.__tela_confirmacao.close()

                if botao_confirmacao == 'confirmar':
                    self.retornar()
                    break
            elif is_operador:
                self.__funcionario = OperadorCaixa("Franco", "12833158904", "teste@gmail", "991300904", "123123as")
                opcoes_operador[opcao_escolhida]()
            else:
                opcoes_supervisor[opcao_escolhida]()
