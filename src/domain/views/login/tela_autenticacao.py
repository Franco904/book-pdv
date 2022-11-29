import re

import PySimpleGUI as sg

from src.domain.exceptions.email_invalido_exception import EmailInvalidoException
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.views.shared.tela_abstrata import Tela


class TelaLogin(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme('Reddit')
        layout = [
            [sg.Text('  ')],
            [sg.Text('Email', size=(10, 1))],
            [sg.InputText(key='email', size=(40, 1))],
            [sg.Text('  ')],
            [sg.Cancel('Voltar', key='voltar', button_color='gray', size=(12, 1)),
             sg.Cancel('Login', key='login', button_color='green', size=(12, 1))],
            [sg.Text('  ')],
        ]

        super().__init__(sg.Window(
            "Login", layout=layout, resizable=False, modal=True, finalize=True, element_justification='c'),
            (200, 100)
        )

    def open(self) -> tuple:
        while True:
            botao, dados = super().read()
            if botao == 'login':
                try:
                    if dados is not None and dados['email'] != '':
                        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', dados['email']):
                            raise EmailInvalidoException
                        else:
                            super().close()
                            break
                    else:
                        raise EntradaVaziaException
                except EntradaVaziaException as e:
                    super().show_message('Campo incompleto!', e)
                except EmailInvalidoException as f:
                    super().show_message('E-mail inválido!', f)
            if botao in ('voltar', sg.WIN_CLOSED):
                super().close()
                break
        return botao, dados
