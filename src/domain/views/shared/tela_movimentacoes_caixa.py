from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaMovimentacoesCaixa(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, movimentacoes: {}) -> None:
        sg.theme('Reddit')

        filtros = ['Todas', 'Vendas', 'Sangrias']

        layout = [
            [sg.Text('Tipo da movimentação', font=('Arial', 12, 'bold'))],
            [
                sg.Combo(
                    filtros,
                    enable_events=True, readonly=True, size=(40, 1),
                    key='tipo_movimentacao', default_value=filtros[0],
                ),
            ],
            [sg.Text('  ')],
            [sg.Text('Movimentações registradas', font=('Arial', 12, 'bold'))],
            [sg.Table(values=movimentacoes['lista'], headings=movimentacoes['colunas'], max_col_width=35,
                      justification='center',
                      num_rows=5,
                      key='movimentacoes_table',
                      row_height=35,
                      tooltip='Movimentações do caixa')],
            [sg.Text('   ')],
            [sg.Cancel('Voltar', key='voltar')],
        ]

        super().__init__(sg.Window('Movimentações do caixa', layout=layout,
                                   resizable=True, finalize=True, modal=True),
                         (500, len(movimentacoes) + 1) * 10)

    def open(self, filter_delegate) -> str | None:
        while True:
            evento, valores = super().read()

            if evento == 'tipo_movimentacao':
                filter_delegate(valores['tipo_movimentacao'])

            if evento == 'voltar' or evento is None or evento == sg.WIN_CLOSED:
                super().close()
                break
        return evento

    def update_component(self, key: str, value) -> None:
        super().update(key, value)
