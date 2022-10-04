from tela_abstrata import Tela
from exceptions.cpf_invalido_exception import CPFInvalidoException
from exceptions.telefone_invalido_exception import TelefoneInvalidoException
from exceptions.nome_invalido_exception import NomeInvalidoException
from exceptions.cpf_ja_cadastrado_exception import CPFJaCadastradoException
from exceptions.entrada_vazia_exception import EntradaVaziaException
from exceptions.email_invalido_exception import EmailInvalidoException
import PySimpleGUI as sg
import re

class TelaCadastroFuncionario(Tela):
    
    def __init__(self, funcionario= None):
        self.__funcionario = funcionario

    def init_components(self):

        sg.theme("Reddit")
        layout = [
                    [sg.Text("Nome:", size=(10,1)), sg.InputText(key='nome', size=(15,1))],
                    [sg.Text("CPF:", size=(10,1)), sg.InputText(key='cpf', size=(15,1))],
                    [sg.Text("E-mail:", size=(10,1)), sg.InputText(key='email', size=(15,1))],
                    [sg.Text("Tel.:", size=(10,1)), sg.InputText(key='telefone', size=(15,1))],
                    [sg.Text("Cargo: (Apenas um)" if self.__funcionario == None else "Alterar cargo? (Apenas um)")],
                    
                    [sg.Radio('Operador de caixa', 'cargo', key='operador', enable_events=True)],
                    [sg.Radio('Supervisor', 'cargo', key='supervisor', enable_events=True)],

                    [sg.Cancel("Voltar", button_color='gray', key='return'), sg.Submit("Enviar", key='enviar', button_color='green')]
                ]

        super().__init__(sg.Window("Novo funcionário" if self.__funcionario == None else "Alterar funcionário", layout=layout, resizable=False, finalize=True), (50,50))


    def open(self, lista_entidade): #verify if its ok to have entity list being used in view
        while True:
            botao, valores = super().read()
            if botao == 'enviar':
                try:
                    if valores is not None and '' not in valores.values():
                        try:
                            if not (valores['cpf'] == None):
                                valores['cpf'] = valores['cpf'].replace('.', '').replace('-', '')
                                valores['telefone'] = valores['telefone'].replace('(', '').replace(')', '').replace('-', '')
                                if valores['cpf'].isnumeric() == False and len(valores['cpf']) != 11:
                                    raise CPFInvalidoException
                                elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', valores['email']): 
                                    raise EmailInvalidoException
                                elif valores['nome'].isascii() == False or valores['nome'].isnumeric() == True:
                                    raise NomeInvalidoException
                                elif len(valores['nome']) < 2 or len(valores['nome']) > 15:
                                    raise NomeInvalidoException
                                elif valores['telefone'].isnumeric() == False and len(valores['telefone']) != 11:
                                    raise TelefoneInvalidoException
                                else:
                                    valores['cpf'] = int(valores['cpf'])
                                    valores['telefone'] = int(valores['telefone'])
                                    if valores['cpf'] in lista_entidade:
                                        raise CPFJaCadastradoException(valores['cpf'])
                                    super().close()
                                    break
                        except CPFInvalidoException as e:
                            super().show_message('Código inválido!', e)
                        except NomeInvalidoException as n:
                            super().show_message("Nome inválido!", n)
                        except CPFJaCadastradoException as f:
                            super().show_message('Código já cadastrado!', f)
                        except EmailInvalidoException as u:
                            super().show_message('E-mail inválido!', u)
                        except TelefoneInvalidoException as t:
                            super().show_message('Telefone inválido!', t)
                    else:
                        raise EntradaVaziaException
                except EntradaVaziaException as g:
                    super().show_message('Campos incompletos!', g)

            elif botao == 'return':
                super().close()
                break

            elif botao in ('return', sg.WIN_CLOSED):
                super().close()
                break

        return botao, valores