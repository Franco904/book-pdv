from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaCadastroCaixa(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, data_horario_criacao) -> None:
        sg.theme('Reddit')

        layout = [
            [sg.Text('Data e horário', size=(24, 0)),
             sg.Text(data_horario_criacao, size=(24, 0), key='data_horario_criacao')],
            [sg.Text('Código:', size=(10, 1)), sg.InputText(key='id', size=(40, 1))],
            [sg.Text('Saldo inicial:', size=(10, 1)), sg.InputText(key='saldo', size=(40, 1))],

            [sg.Text('       ')],
            [sg.Push(), sg.Cancel('Voltar', button_color='gray', key='voltar', size=(12, 1)),
             sg.Submit('Enviar', key='enviar', button_color='green', size=(12, 1))]
        ]

        super().__init__(sg.Window('Novo caixa', layout=layout, resizable=False, finalize=True), (400, 150))

    def open(self) -> tuple:
        while True:
            botao, valores = super().read()

            if botao == 'enviar':
                super().close()
                break

            if botao in ('voltar', None, sg.WIN_CLOSED):
                super().close()
                break
        return botao, valores
