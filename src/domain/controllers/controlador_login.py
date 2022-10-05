import PySimpleGUI as sg
import pandas as pd

from src.domain.views.login.tela_home import TelaHome
from src.domain.views.login.tela_login import TelaLogin
from src.domain.views.login.tela_senha import TelaSenha


class ControladorLogin:
    def __init__(self, controlador_sistema, login_dao: LoginDAO) -> None:
        self.__tela_home = TelaHome()
        self.__tela_login = TelaLogin()
        self.__tela_senha = TelaSenha()
        self.__controlador_sistema = controlador_sistema
        self.__login_dao = login_dao

    def entrar(self):
        pass

    def retornar(self):
        self.__tela_.close()

    def sair(self):
        exit(0)

    def abre_tela(self):
        opcoes = {1: self.entrar , 2: self.fechar}

        while True:
            self.__tela_home.init_components()
            opcao_escolhida = self.__tela_home.open()
            self.__tela_funcionarios.close()

            if opcao_escolhida == 5 or opcao_escolhida is None or sg.WIN_CLOSED:
                self.__tela_funcionarios.close()
                break
            else:
                opcoes[opcao_escolhida]()

    def abre_inicio(self):
        # Implement controls to inicio
        is_operador = True

        self.__controlador_sistema.controllers["inicio"].abre_tela(is_operador=is_operador)
