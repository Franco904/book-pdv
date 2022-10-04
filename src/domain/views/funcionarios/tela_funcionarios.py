from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaFuncionarios(Tela):

    def __init__(self):
        pass

    def init_components(self):
        sg.theme("Reddit")
        layout = [
                    [sg.Submit("Cadastrar novo funcionário", key=1)],
                    [sg.Submit("Listar funcionários", key=2)],
                    [sg.Submit("Alterar funcionário", key=3)],
                    [sg.Submit("Excluir funcionário", key=4)],
                    [sg.Cancel("Voltar", key=5, button_color='gray'), sg.Cancel('Sair', key=0, button_color='red')]
                ]

        super().__init__(sg.Window("Módulo Funcionários", layout=layout, resizable=False, modal=True, finalize=True), (200,200))

    def open(self):
        while True:
            botao, valores = super().read()
            if botao == None or botao == sg.WIN_CLOSED or botao == 5:
                super().close()
                break
            
        return botao
