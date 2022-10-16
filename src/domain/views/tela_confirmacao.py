from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaConfirmacao(Tela):
    def __init__(self):
        pass

    def init_components(self):
        sg.theme("Reddit")
        layout = [
                    [sg.Text("  ")],
                    [sg.Text("Deseja realmente continuar com a operação?")],
                    [sg.Text("  ")],
                    [sg.Cancel("Cancelar", key='cancel', button_color='red', size=(12, 1)), sg.Cancel('Confirmar', key='confirmar', button_color='green', size=(12, 1))]
                ]

        super().__init__(sg.Window("Confirmação", layout=layout, resizable=False, modal=True, finalize=True, element_justification='c'), (200,100))

    def open(self):
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'cancel':
                super().close()
                break
            return botao
