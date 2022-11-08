from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaHome(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme('Reddit')
        layout = [
                    [sg.Text('  ')],
                    [sg.Cancel('Entrar', key="entrar", button_color='green', size=(12, 1))],
                    [sg.Text('  ')],
                    [sg.Cancel('Fechar', key="fechar", button_color='gray', size=(12, 1))],
                    [sg.Text('  ')]
                  ]

        super().__init__(sg.Window('Home', layout=layout, resizable=False, modal=True, finalize=True, element_justification='c'), (200,100))

    def open(self) -> str:
        while True:
            botao, dados = super().read()

            if botao == 'entrar' or botao in ('fechar', None, sg.WIN_CLOSED):
                super().close()
                break

        return botao
