from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaBuscarCaixa(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme("Reddit")
        layout = [

                    [sg.Cancel("Voltar", key='voltar')]
                ]

        super().__init__(sg.Window('Buscar caixa', layout=layout, resizable=True, finalize=True, modal=True),(200,(len(lista_entidades)+1)*10) )

    def open(self) -> str | None:
        while True:
            botao, valores = super().read()
            if botao == 'voltar' or botao is None or botao == sg.WIN_CLOSED:
                super().close()
                break
        return botao
