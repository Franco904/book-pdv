from src.domain.views.tela_abstrata import Tela
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.exceptions.desconto_invalido_exception import DescontoInvalidoException
import PySimpleGUI as sg


class TelaDesconto(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme("Reddit")
        layout = [
                    [sg.Text("  ")],
                    [
                        [sg.Radio('Aplicar', 'operacao', key='aplicar', enable_events=True, size=(20, 1))],
                        [sg.Radio('Remover', 'operacao', key='remover', enable_events=True, size=(20, 1))]
                    ],
                    [sg.Text("Valor do desconto (%): ", key='input_text', visible=False),
                     sg.InputText(key='valor_desconto', size=(20, 1), visible=False)],
                    [sg.Text("  ")],
                    [sg.Cancel("Voltar", key='return', button_color='gray', size=(12, 1)),
                     sg.Cancel('Salvar', key='salvar', button_color='green', size=(12, 1))],
                ]

        super().__init__(sg.Window("Buscar produto", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'))

    def open(self) -> tuple:
        while True:
            evento, valores = super().read()

            remover = False
            if valores['aplicar']:
                super().window['input_text'].update(visible=True)
                super().window['valor_desconto'].update(visible=True)
            else:
                remover = True
                super().window['input_text'].update(visible=False)
                super().window['valor_desconto'].update(visible=False)

            if evento == 'salvar':
                if not remover:
                    try:
                        if not valores['valor_desconto'] == '':
                            if valores['valor_desconto'].isnumeric() is False:
                                raise DescontoInvalidoException
                            valores['valor_desconto'] = int(valores['valor_desconto'])
                            if valores['valor_desconto'] < 0 or valores['valor_desconto'] > 100:
                                raise DescontoInvalidoException
                            super().close()
                            break
                        else:
                            raise EntradaVaziaException

                    except EntradaVaziaException as e:
                        super().show_message("Campos incompletos!", e)
                    except DescontoInvalidoException as d:
                        super().show_message("Desconto inválido!", d)
                else:
                    super().close()
                    break

            if evento is None or evento == sg.WIN_CLOSED or evento == 'return':
                super().close()
                break

        return evento, valores
