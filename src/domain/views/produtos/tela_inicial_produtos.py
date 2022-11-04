from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaIncialProdutos(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, livros: {}, eletronicos: {}, is_supervisor: bool = False) -> None:

        sg.theme("Reddit")

        button_group = [
            [
                sg.Cancel("Voltar", key='voltar'),
                sg.Submit('Editar', key='editar'),
                sg.Submit('Excluir', key='excluir'),
                sg.Submit('Aplicar/Remover desconto', key='desconto'),
                sg.Submit('Novo', key='novo', button_color='green')
            ]
        ] if is_supervisor else [
            [sg.Cancel("Voltar", key='voltar')]
        ]

        layout = [

            [
                [sg.Text('Livros', font=('Arial', 12, 'bold'))],
                [sg.Table(values=livros['lista'], headings=livros['colunas'], max_col_width=35,
                          auto_size_columns=True,
                          display_row_numbers=False,
                          justification='center',
                          num_rows=len(livros['lista']),
                          key='tabela_livros',
                          row_height=35,
                          tooltip='Lista de livros')]
                if len(livros['lista']) else [sg.Text('Não existem Livros cadastrados.')],

                [sg.Text('   ')],

                [sg.Text('Eletrônicos', font=('Arial', 12, 'bold'))],
                [sg.Table(values=eletronicos['lista'], headings=eletronicos['colunas'], max_col_width=35,
                          auto_size_columns=True,
                          display_row_numbers=False,
                          justification='center',
                          num_rows=len(eletronicos['lista']),
                          key='tabela_eletronicos',
                          row_height=35,
                          tooltip='Lista de eletrônicos')]
                if len(eletronicos['lista']) else [sg.Text('Não existem Eletrônicos cadastrados.')]
            ]
            if len(livros['lista']) + len(eletronicos['lista']) != 0 else [
                [sg.Text('   ')],
                [sg.Text('Não existem Produtos cadastrados.', font=('Arial', 10, 'bold'))]],

            [sg.Text('   ')],
            button_group
        ]

        super().__init__(sg.Window('Produtos', layout=layout,
                                   resizable=True, finalize=True, modal=True),
                         (300, (len(livros) + len(eletronicos) + 1) * 10))

    def open(self) -> str | None:
        while True:
            botao, valores = super().read()

            if botao in ('editar', 'excluir', 'desconto', 'novo'):
                super().close()
                break

            if botao == 'voltar' or botao is None or botao == sg.WIN_CLOSED:
                super().close()
                break
        return botao
