from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaGerirCaixas(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme("Reddit")
        layout = [
            [sg.Submit("Cadastrar caixa", key='cadastrar', size=(20, 1))],
            [sg.Submit("Inativar caixa", key='inativar', size=(20, 1))],
            [sg.Submit("Histórico de aberturas", key='aberturas', size=(20, 1))],
            [sg.Submit("Histórico de movimentações", key='movimentacoes', size=(20, 1))],
            [sg.Cancel("Voltar", key='voltar', button_color='gray', size=(9, 1))]
        ]

        super().__init__(sg.Window('Caixas', layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 180))

    def open(self) -> str | None:
        while True:
            botao, valores = super().read()

            if botao in ('cadastrar', 'inativar', 'aberturas', 'movimentacoes'):
                super().close()
                break

            if botao in ('voltar', None, sg.WIN_CLOSED):
                super().close()
                break
        return botao
