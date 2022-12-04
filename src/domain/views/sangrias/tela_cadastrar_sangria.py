import PySimpleGUI as sg
from src.domain.views.shared.tela_abstrata import Tela
from src.domain.exceptions.sangrias.sangria_invalida_exception import SangriaInvalidaException
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException


class TelaCadastrarSangrias(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, data: str, saldo_atual: float | int) -> None:
        sg.theme("Reddit")
        layout = [
            [sg.Text("  ")],
            [sg.Text("Data: "), sg.Text(data)],
            [sg.Text(f'Saldo atual do caixa: {saldo_atual}')],
            [sg.Text("Valor da sangria: "), sg.InputText(key='valor_sangria', size=(10, 1))],
            [sg.Multiline(size=(30, 5), pad=(5, 5), key='observacao_sangria')],
            [sg.Text("  ")],
            [sg.Cancel("Voltar", key='return', button_color='gray', size=(12, 1)),
             sg.Cancel('Enviar', key='enviar', button_color='green', size=(12, 1))],
        ]

        super().__init__(sg.Window("Nova Sangria", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='l'), (200, 300))

    def open(self, saldo_atual: float) -> tuple:
        while True:
            botao, valores = super().read()

            if botao == 'enviar':
                try:
                    if not valores['valor_sangria'] == '':
                        if valores['valor_sangria'].isnumeric() is False:
                            raise SangriaInvalidaException
                        valores['valor_sangria'] = float(valores['valor_sangria'])
                        if valores['valor_sangria'] <= 0 or valores['valor_sangria'] > saldo_atual:
                            raise SangriaInvalidaException
                        break
                    else:
                        raise EntradaVaziaException

                except EntradaVaziaException as e:
                    super().show_message("Campos incompletos!", e)
                except SangriaInvalidaException as s:
                    super().show_message("Sangria Inválida!", s)

            if botao is None or botao == sg.WIN_CLOSED or botao == 'return':
                super().close()
                break

        return botao, valores
