from src.domain.views.tela_abstrata import Tela
from src.domain.exceptions.cpf_invalido_exception import CPFInvalidoException
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.exceptions.cpf_inexistente import CPFInexistenteException
import PySimpleGUI as sg


class TelaBuscaFuncionario(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self) -> None:
        sg.theme("Reddit")
        layout = [
                    [sg.Text("  ")],
                    [sg.Text("CPF do funcionário: "), sg.InputText(key='busca_cpf', size=(20, 1))],
                    [sg.Text("  ")],
                    [sg.Cancel("Voltar", key='return', button_color='gray', size=(12, 1)), sg.Cancel('Buscar', key='buscar', button_color='green', size=(12, 1))],
                ]

        super().__init__(sg.Window("Buscar funcionário", layout=layout, resizable=False, modal=True, finalize=True, element_justification='c'), (200,100))

    def open(self) -> tuple:
        while True:
            botao, valores = super().read()

            if botao == 'buscar':
                try:
                    if not valores['busca_cpf'] == '':
                        valores['busca_cpf'].replace('.', '').replace('-', '')
                        if valores['busca_cpf'].isnumeric() is False or not len(valores['busca_cpf']) == 11:
                            raise CPFInvalidoException
                        super().close()
                        break
                    else:
                        raise EntradaVaziaException

                except EntradaVaziaException as e:
                    super().show_message("Digite um CPF para buscar!", e)
                except CPFInvalidoException as c:
                    super().show_message("CPF inválido!", c)
                except CPFInexistenteException as i:
                    super().show_message('CPF não encontrado!', i)

            if botao is None or botao == sg.WIN_CLOSED or botao == 'return':
                super().close()
                break

        return botao, valores['busca_cpf']
