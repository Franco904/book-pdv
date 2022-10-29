import PySimpleGUI as sg

from src.domain.models.caixa import Caixa
from src.domain.views.tela_abstrata import Tela


class TelaAbrirCaixa(Tela):
    def __init__(self):
        pass

    def init_components(self, caixas_ids=None, data_abertura=None):
        if caixas_ids is None or data_abertura is None:
            return

        sg.theme('Reddit')
        layout = [
            [sg.Combo(caixas_ids, enable_events=True, readonly=True, size=(40, 1), key='caixa_id')],

            [sg.Text('Data', size=(24, 0), font=('', 10)),
             sg.Text(data_abertura, size=(24, 0), font=('', 10), key='data_abertura')],
            [sg.Text('Valor', size=(24, 0), font=('', 10)),
             sg.Text('-', size=(24, 0), font=("", 10), key='saldo_abertura')],
            [sg.Text('Observações', size=(24, 0), font=('', 10))],
            [sg.Multiline(size=(50, 5), pad=(5, 5), key='observacoes')],
            [sg.Push(), sg.Cancel('Voltar', key='voltar', button_color='gray'),
             sg.Cancel('Abrir caixa', key='abrir_caixa', button_color='green')]
        ]

        super().__init__(sg.Window('Abrir caixa', layout=layout, resizable=False, finalize=True))

    def open(self, caixas: [Caixa] = None):
        if caixas is None:
            return

        while True:
            evento, dados = super().read()

            # Voltar
            if evento in ('voltar', None, sg.WIN_CLOSED):
                super().close()
                break

            # Atualiza dinamicamente o valor de saldo, conforme seleção no combo de caixas
            elif evento == 'caixa_id':
                id = dados['caixa_id']
                saldo = list(filter(lambda caixa: caixa.id == id, caixas))[0].saldo

                super().update('saldo_abertura', saldo)

            # Abrir caixa
            elif evento == 'abrir_caixa':
                if dados['caixa_id'] == '':
                    super().show_message('Atenção!', 'Preencha o campo Caixa corretamente!')
                    continue
                break

        super().close()
        return evento, dados

    def close(self):
        super().close()
