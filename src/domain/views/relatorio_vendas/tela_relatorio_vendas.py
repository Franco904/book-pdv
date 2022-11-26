from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaRelatorioVendas(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, vendas: {}, filter_delegate) -> None:
        sg.theme('Reddit')

        filter_options = [
            'Última semana',
            'Último mês',
            'Últimos 3 meses',
            'Último ano',
            'Últimos 5 anos',
        ]

        button_group = [
            [
                sg.Cancel('Voltar', key='voltar'),
                sg.Submit('Ver informações dos produtos', key='venda_produtos', button_color='green'),
                sg.Submit('Produtos mais vendidos', key='mais_vendidos', button_color='green'),
            ]
        ]

        layout = [
            [
                [sg.Combo(
                    filter_options,
                    enable_events=True, readonly=True, size=(40, 1),
                    key='filter_option', default_value=filter_options[0])],
                [
                    sg.Text(f'{"+" if vendas["diff_registros"] > 0 else ""} {vendas["diff_registros"]}',
                            size=(24, 0), font=('', 10), key='diff_registros'),
                    sg.Text(' registros desde o último período', size=(24, 0), font=('', 10))
                ],
                [
                    sg.Text(f'{"+" if vendas["diff_registros"] > 0 else ""} R$ {vendas["diff_receita"]}',
                            size=(24, 0), font=('', 10), key='diff_receita'),
                    sg.Text(' de receita em comparação com o último período', size=(24, 0), font=('', 10))
                ],
                [
                    sg.Text('O funcionário que realizou mais vendas foi ', size=(24, 0), font=('', 10)),
                    sg.Text(vendas['operador_com_mais_vendas']['nome'],
                            size=(24, 0), font=('', 10), key='operador_com_mais_vendas'),
                    sg.Text(' com um total de R$ ', size=(24, 0), font=('', 10)),
                    sg.Text(f'{vendas["operador_com_mais_vendas"]["total"]}', size=(24, 0), font=('', 10)),
                ],
                [sg.Table(values=vendas['lista'], headings=vendas['colunas'], max_col_width=35,
                          auto_size_columns=True,
                          display_row_numbers=False,
                          justification='center',
                          num_rows=len(vendas['lista']),
                          key='vendas_table',
                          row_height=35,
                          tooltip='Vendas no período')]
                if len(vendas['lista']) else [sg.Text('Não existem vendas cadastradas.')],
            ],

            [sg.Text('   ')],
            button_group
        ]

        super().__init__(sg.Window('Relatório de vendas por período', layout=layout,
                                   resizable=True, finalize=True, modal=True),
                         (300, len(vendas) + 1) * 10)

    def open(self) -> str | None:
        while True:
            botao, valores = super().read()

            if botao in ('venda_produtos', 'mais_vendidos'):
                super().close()
                break

            if botao == 'voltar' or botao is None or botao == sg.WIN_CLOSED:
                super().close()
                break
        return botao
