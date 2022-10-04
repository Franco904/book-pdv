from tela_abstrata import Tela
from exceptions.cpf_invalido_exception import CPFInvalidoException
from exceptions.entrada_vazia_exception import EntradaVaziaException
from exceptions.cpf_inexistente import CPFInexistenteException
import PySimpleGUI as sg

class TelaBuscaFuncionario(Tela):

    def __init__(self):
        pass

    def init_components(self):
        sg.theme("Reddit")
        layout = [
                    [sg.Text("CPF do funcionário: "), sg.InputText(key='busca_cpf', size=(15,1))],
                    [sg.Cancel("Voltar", key='return', button_color='gray'), sg.Cancel('Buscar', key='buscar', button_color='green')]
                ]

        super().__init__(sg.Window("Buscar funcionário", layout=layout, resizable=False, modal=True, finalize=True), (200,200))

    def open(self, lista_entidade): #verify if its ok to have entity list being used in view
        while True:
            botao, valores = super().read()

            if botao == 'buscar':
                try:
                    if not valores['busca_cpf'] == '':
                        valores['busca_cpf'].replace('.', '').replace('-', '')
                        if valores['busca_cpf'].isnumeric() == False and len(valores['busca_cpf']) != 11:
                            raise CPFInvalidoException

                        if valores['busca_cpf'] not in lista_entidade:
                            raise CPFInexistenteException
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

            if botao == None or botao == sg.WIN_CLOSED or botao == 'return':
                super().close()
                break

        return botao, valores
