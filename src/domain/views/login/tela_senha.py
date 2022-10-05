from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg

class TelaSenha(Tela):

    def __init__(self):
        pass



    def init_components(self):
        sg.theme("Reddit")
        layout = [
                    [sg.Text("  ")],
                    [sg.Text("Senha:", size=(10, 1)), sg.InputText(key='email', size=(40, 1))],
                    [sg.Cancel("Voltar", key='return', button_color='gra', size=(12, 1))],
                    [sg.Cancel('Login', key='close ', button_color='green', size=(12, 1))]
                  ]

        super().__init__(sg.Window("Home", layout=layout, resizable=False, modal=True, finalize=True, element_justification='c'), (200,100))


    def open(self):
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'cancel':
                super().close()
                break
            return botao