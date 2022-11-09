from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg

class TelaInicialVenda(Tela):

    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme("Reddit")
        layout = [
            [sg.Submit("Cadastrar venda", key='cadastrar', size=(20, 1))],
            [sg.Submit("Alterar venda", key='alterar', size=(20, 1))],
            [sg.Submit("Cancelar venda", key='cancelar', size=(20, 1))],
            [sg.Cancel("Voltar", key='voltar', button_color='gray', size=(9, 1))]
        ]

        super().__init__(sg.Window("Venda", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 180))


    def open(self) -> str | None:
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'voltar':
                super().close()
                break

            return botao

#retirar depois
tela = TelaInicialVenda()
tela.init_components()
opcao, dados = tela.open()