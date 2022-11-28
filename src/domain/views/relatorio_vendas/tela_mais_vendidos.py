from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaProdutosMaisVendidos(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, produtos: {}) -> None:
        sg.theme("Reddit")

        layout = [
            [sg.Text('Relação por categoria', font=('Arial', 12, 'bold'))],
            [sg.Text(f'{produtos["percentual_livros"]}% Livros / Revistas / Similares')],
            [sg.Text(f'{produtos["percentual_eletronicos"]}% Eletrônicos / Diversos')],
            [sg.Text('   ')],
            [sg.Text('Produtos mais vendidos no período', font=('Arial', 12, 'bold'))],
            [sg.Table(values=produtos['lista'], headings=produtos['colunas'], max_col_width=35,
                      auto_size_columns=True,
                      display_row_numbers=False,
                      justification='center',
                      num_rows=5,
                      key='produtos_venda_table',
                      row_height=35,
                      tooltip='Produtos mais vendidos no período')]
            if len(produtos['lista']) else [sg.Text('Não houve produtos cadastrados no período.')],
            [sg.Text('   ')],
            [sg.Cancel('Voltar', key='voltar')],
        ]

        super().__init__(sg.Window('Produtos mais vendidos no período', layout=layout,
                                   resizable=True, finalize=True, modal=True),
                         (300, (len(produtos) + 1) * 10))

    def open(self) -> str | None:
        while True:
            botao, valores = super().read()

            if botao == 'voltar' or botao is None or botao == sg.WIN_CLOSED:
                super().close()
                break
        return botao
