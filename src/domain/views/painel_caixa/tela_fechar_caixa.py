import PySimpleGUI as sg

from src.domain.views.tela_abstrata import Tela


class TelaFecharCaixa(Tela):
    def __init__(self):
        pass

    def init_components(self, dados_caixa=None) -> None:
        sg.theme('Reddit')
        layout = [
            [sg.Text('Código do caixa', size=(24, 0), font=('', 10)),
             sg.Text(dados_caixa['id_caixa'], size=(24, 0), font=('', 10))],
            [sg.Text('Data e horário', size=(24, 0), font=('', 10)),
             sg.Text(dados_caixa['data_horario_fechamento'].strftime("%d/%m/%Y, %H:%M"), size=(24, 0), font=('', 10), key='data_horario_fechamento')],
            [sg.Text('Saldo de fechamento', size=(24, 0), font=('', 10)),
             sg.Text(f'R$ {dados_caixa["saldo_fechamento"]}', size=(24, 0), font=("", 10), key='saldo_fechamento')],
            [sg.Text('Observação', size=(24, 0), font=('', 10))],
            [sg.Multiline(size=(50, 5), pad=(5, 5), key='observacao_fechamento')],
            [sg.Push(), sg.Cancel('Voltar', key='voltar', button_color='gray'),
             sg.Cancel('Fechar caixa', key='fechar_caixa', button_color='green')]
        ]

        super().__init__(sg.Window('Fechar caixa', layout=layout, resizable=False, finalize=True))

    def open(self) -> tuple:
        while True:
            evento, dados = super().read()

            # Voltar
            if evento in ('voltar', None, sg.WIN_CLOSED):
                super().close()
                break

            if evento == 'fechar_caixa':
                break

        return evento, dados

    def close(self) -> None:
        super().close()

    def show_form_confirmation(self, titulo: str, msg) -> str:
        while True:
            botao_confirmacao = super().show_form_confirmation(titulo, msg)

            if botao_confirmacao in ('OK', 'Cancel', None, sg.WIN_CLOSED):
                break

        return botao_confirmacao
