from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaVendaProdutos(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, produtos: {}) -> None:
        sg.theme("Reddit")

        layout = [
            [sg.Text('Código da venda', font=('Arial', 12, 'bold'))],
            [sg.Text(f'{produtos["id_venda"]}')],
            [sg.Text('   ')],
            [sg.Text('Produtos registrados', font=('Arial', 12, 'bold'))],
            [sg.Table(values=produtos['lista'], headings=produtos['colunas'], max_col_width=35,
                      auto_size_columns=True,
                      display_row_numbers=False,
                      justification='center',
                      num_rows=5,
                      key='produtos_venda_table',
                      row_height=35,
                      tooltip='Produtos registrados na venda')]
            if len(produtos['lista']) else [sg.Text('Não existem produtos cadastradas nesta venda.')],
            [sg.Text('   ')],
            [sg.Cancel('Voltar', key='voltar')],
        ]

        super().__init__(sg.Window('Produtos registrados na venda', layout=layout,
                                   resizable=True, finalize=True, modal=True),
                         (300, (len(produtos) + 1) * 10))

    def open(self) -> str | None:
        while True:
            botao, valores = super().read()

            if botao == 'voltar' or botao is None or botao == sg.WIN_CLOSED:
                super().close()
                break
        return botao
