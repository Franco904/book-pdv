from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg

class TelaHome(Tela):

    def __init__(self):
        pass


    def init_components(self):
        sg.theme("Reddit")
        layout = [
                    [sg.Cancel("Entrar", key='entrar', button_color='green', size=(12, 1))],
                    [sg.Text("  ")],
                    [sg.Cancel('Fechar', key='close ', button_color='gray', size=(12, 1))]
                  ]

        super().__init__(sg.Window("Home", layout=layout, resizable=False, modal=True, finalize=True, element_justification='c'), (200,100))


    def open(self):
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'cancel':
                super().close()
                break
            return botao


test = TelaHome()
test.init_components()
opcao_escolhida = test.open()
test.close()