from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaRelatorioVendas(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, vendas: {}) -> None:
        sg.theme('Reddit')

        periodos = [
            'Última semana',
            'Último mês',
            'Últimos 3 meses',
            'Último ano',
            'Últimos 5 anos',
        ]

        button_group = [
            sg.Cancel('Voltar', key='voltar'),
            sg.Submit('Ver informações dos produtos', key='venda_produtos', button_color='green'),
            sg.Submit('Produtos mais vendidos', key='mais_vendidos', button_color='green'),
        ]

        layout = [
            [sg.Text('Período', font=('Arial', 12, 'bold'))],
            [
                sg.Combo(
                    periodos,
                    enable_events=True, readonly=True, size=(40, 1),
                    key='periodo', default_value=periodos[0],
                ),
            ],
            [sg.Text('  ')],
            [sg.Text('Estatísticas', font=('Arial', 12, 'bold'))],
            [
                sg.Text(f'{"+" if vendas["diff_registros"] > 0 else ""} {vendas["diff_registros"]}',
                        font=('', 10), key='diff_registros'),
                sg.Text(' registros desde o último período', font=('', 10))
            ],
            [
                sg.Text(f'{"+" if vendas["diff_receita"] > 0 else ""} R$ {round(vendas["diff_receita"], 2)}',
                        font=('', 10), key='diff_receita'),
                sg.Text(' de receita em comparação com o último período', size=(24, 0), font=('', 10))
            ],
            [
                sg.Text('O funcionário que realizou mais vendas foi ', font=('', 10)),
                sg.Text(vendas['operador_com_mais_vendas']['nome'], font=('', 10), key='operador_nome'),
                sg.Text(' com um total de', font=('', 10)),
                sg.Text(f' R$ {vendas["operador_com_mais_vendas"]["total"]}', font=('', 10), key='operador_total'),
            ],
            [sg.Text('  ')],
            [sg.Text('Vendas registradas', font=('Arial', 12, 'bold'))],
            [sg.Table(values=vendas['lista'], headings=vendas['colunas'], max_col_width=35,
                      auto_size_columns=True,
                      display_row_numbers=False,
                      justification='center',
                      num_rows=5,
                      key='vendas_table',
                      row_height=35,
                      tooltip='Vendas no período')]
            if len(vendas['lista']) else [sg.Text('Não existem vendas cadastradas.')],
            [sg.Text('   ')],
            button_group,
        ]

        super().__init__(sg.Window('Relatório de vendas por período', layout=layout,
                                   resizable=True, finalize=True, modal=True),
                         (300, len(vendas) + 1) * 10)

    def open(self, filter_delegate) -> str | None:
        while True:
            evento, valores = super().read()

            if evento == 'periodo':
                filter_delegate(valores['periodo'])

            if evento in ('venda_produtos', 'mais_vendidos'):
                super().close()
                break

            if evento == 'voltar' or evento is None or evento == sg.WIN_CLOSED:
                super().close()
                break
        return evento

    def update_component(self, key: str, value) -> None:
        super().update(key, value)
