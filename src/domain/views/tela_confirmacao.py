from tela_abstrata import Tela
import PySimpleGUI as sg

class TelaConfirmacao(Tela):

    def __init__(self):
        pass

    def init_components(self):
        sg.theme("Reddit")
        layout = [
                    [sg.Text("Deseja realmente continuar com a operação?")],
                    [sg.Cancel("Cancelar", key='cancel', button_color='red'), sg.Cancel('Confirmar', key='confirmar', button_color='green')]
                ]

        super().__init__(sg.Window("Confirmação", layout=layout, resizable=False, modal=True, finalize=True), (200,200))

    def open(self):
        while True:
            botao, valores = super().read()
            if botao == None or botao == sg.WIN_CLOSED or botao == 'cancel':
                super().close()
                break

        return botao
