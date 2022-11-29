from src.domain.views.shared.tela_abstrata import Tela
from src.domain.exceptions.codigo_invalido_exception import CodigoInvalidoException
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
import PySimpleGUI as sg


class TelaBuscaProduto(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme("Reddit")
        layout = [
                    [sg.Text("  ")],
                    [sg.Text("Código do produto: "), sg.InputText(key='busca_codigo_produto', size=(20, 1))],
                    [sg.Text("  ")],
                    [sg.Cancel("Voltar", key='return', button_color='gray', size=(12, 1)),
                     sg.Cancel('Buscar', key='buscar', button_color='green', size=(12, 1))],
                ]

        super().__init__(sg.Window("Buscar produto", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (200, 100))

    def open(self) -> tuple:
        while True:
            botao, valores = super().read()

            if botao == 'buscar':
                try:
                    if not valores['busca_codigo_produto'] == '':
                        if valores['busca_codigo_produto'].isnumeric() is False:
                            raise CodigoInvalidoException('produto')
                        valores['busca_codigo_produto'] = int(valores['busca_codigo_produto'])
                        break
                    else:
                        raise EntradaVaziaException

                except EntradaVaziaException as e:
                    super().show_message("Digite um código para buscar!", e)
                except CodigoInvalidoException as c:
                    super().show_message("Código inválido!", c)

            if botao is None or botao == sg.WIN_CLOSED or botao == 'return':
                super().close()
                break

        return botao, valores['busca_codigo_produto']
