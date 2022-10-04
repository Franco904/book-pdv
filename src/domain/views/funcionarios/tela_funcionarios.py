from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaFuncionarios(Tela):

    def __init__(self):
        pass

    def init_components(self):
        sg.theme("Reddit")
        layout = [
                    [sg.Submit("Cadastrar novo funcionário", key=1, size=(20, 1))],
                    [sg.Submit("Listar funcionários", key=2, size=(20, 1))],
                    [sg.Submit("Alterar funcionário", key=3, size=(20, 1))],
                    [sg.Submit("Excluir funcionário", key=4, size=(20, 1))],
                    [sg.Cancel("Voltar", key=5, button_color='gray', size=(9, 1)), sg.Cancel('Sair', key=0, button_color='red', size=(9, 1))]
                ]

        super().__init__(sg.Window("Módulo Funcionários", layout=layout, resizable=False, modal=True, finalize=True, element_justification='c'), (300,180))
        
    def open(self):
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 5:
                super().close()
                break
            if botao == 0:
                exit(0)

            return botao
