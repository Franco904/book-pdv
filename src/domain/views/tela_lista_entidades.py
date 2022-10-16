from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaListaEntidades(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, lista_entidades, nome_colunas, nome_tela) -> None:

        sg.theme("Reddit")
        layout = [
                    [sg.Table(values=lista_entidades, headings=nome_colunas, max_col_width=35,
                              auto_size_columns=True,
                              display_row_numbers=False,
                              justification='center',
                              num_rows=len(lista_entidades),
                              key='tabela_entidades',
                              row_height=35,
                              tooltip=nome_tela)],
                    [sg.Cancel("Voltar", key='voltar')]
                ]

        super().__init__(sg.Window(nome_tela, layout=layout, resizable=True, finalize=True, modal=True),(200,(len(lista_entidades)+1)*10) )

    def open(self) -> str | None:
        while True:
            botao, valores = super().read()
            if botao == 'voltar' or botao is None or botao == sg.WIN_CLOSED:
                super().close()
                break
        return botao
