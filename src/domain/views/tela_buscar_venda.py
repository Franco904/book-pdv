from src.domain.exceptions.codigo_invalido_exception import CodigoInvalidoException
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaBuscaVenda(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme("Reddit")
        layout = [
            [sg.Text("   ")],
            [sg.Text("Código da Venda"),
             sg.InputText(key='codigo_venda', size=(22, 1))],
            [sg.Text("   ")],
            [sg.Cancel("Voltar", key='voltar', button_color='gray', size=(9, 1)),
             sg.Submit("Buscar", key='buscar', size=(20, 1))]
        ]

        super().__init__(sg.Window("Buscar Produto", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 80))

    def open(self):
        while True:
            botao, valores = super().read()
            if botao == 'buscar':
                try:
                    if not valores['codigo_venda'] == '':
                        if valores['codigo_venda'].isnumeric() == False:
                            raise CodigoInvalidoException('venda')
                        valores['codigo_venda'] = int(valores['codigo_venda'])
                        break
                    else:
                        raise EntradaVaziaException

                except EntradaVaziaException as e:
                    super().show_message("Digite um código para buscar!", e)
                except CodigoInvalidoException as c:
                    super().show_message("Código Inválido!", c)


            if botao is None or botao == sg.WIN_CLOSED or botao == 'voltar':
                super().close()
                break

            return botao, valores['codigo_venda']



