from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaAberturasCaixa(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, aberturas: {}) -> None:
        sg.theme('Reddit')

        layout = [
            [sg.Text('Operador', font=('Arial', 12, 'bold'))],
            [
                sg.Combo(
                    [f.capitalize() for f in aberturas['filtros']],
                    enable_events=True, readonly=True, size=(40, 1),
                    key='operador', default_value=aberturas['filtros'][0],
                ),
            ],
            [sg.Text('  ')],
            [sg.Text('Aberturas registradas', font=('Arial', 12, 'bold'))],
            [sg.Table(values=aberturas['lista'], headings=aberturas['colunas'], max_col_width=30,
                      vertical_scroll_only=False,
                      justification='center',
                      num_rows=5,
                      key='aberturas_table',
                      row_height=35,
                      tooltip='Vendas no período')],
            [sg.Text('   ')],
            [sg.Cancel('Voltar', key='voltar')],
        ]

        super().__init__(sg.Window('Aberturas do caixa', layout=layout,
                                   resizable=True, finalize=True, modal=True),
                         (500, len(aberturas) + 1) * 10)

    def open(self, filter_delegate, operadores: list, id_caixa: int) -> str | None:
        while True:
            evento, valores = super().read()

            if evento == 'operador':
                filter_delegate(valores['operador'], operadores, id_caixa)

            if evento == 'voltar' or evento is None or evento == sg.WIN_CLOSED:
                super().close()
                break
        return evento

    def update_component(self, key: str, value) -> None:
        super().update(key, value)
