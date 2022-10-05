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
            self.__tela_login.init_components()
            opcao_escolhida = self.__tela_login.open()
            self.__tela_login.close()

            if opcao_escolhida == 2 or opcao_escolhida is None or sg.WIN_CLOSED:
                self.__tela_login.close()
                break
            else:
                opcoes[opcao_escolhida]()

