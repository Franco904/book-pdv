import PySimpleGUI as sg

from src.domain.views.tela_abstrata import Tela


class TelaFuncionarios(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme("Reddit")
        layout = [
            [sg.Submit("Cadastrar novo funcionário", key='cadastrar', size=(20, 1))],
            [sg.Submit("Listar funcionários", key='listar', size=(20, 1))],
            [sg.Submit("Alterar funcionário", key='alterar', size=(20, 1))],
            [sg.Submit("Excluir funcionário", key='excluir', size=(20, 1))],
            [sg.Cancel("Voltar", key='voltar', button_color='gray', size=(9, 1))]
        ]

        super().__init__(sg.Window("Módulo Funcionários", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 180))

    def open(self) -> str:
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'voltar':
                super().close()
                break

            return botao
