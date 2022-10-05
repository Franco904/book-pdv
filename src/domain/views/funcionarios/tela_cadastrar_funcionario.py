from ..tela_abstrata import Tela
from src.domain.exceptions.cpf_invalido_exception import CPFInvalidoException
from src.domain.exceptions.telefone_invalido_exception import TelefoneInvalidoException
from src.domain.exceptions.nome_invalido_exception import NomeInvalidoException
from src.domain.exceptions.cpf_ja_cadastrado_exception import CPFJaCadastradoException
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.exceptions.email_invalido_exception import EmailInvalidoException
from src.domain.exceptions.cargo_invalido_exception import CargoInvalidoException
import PySimpleGUI as sg
import re

class TelaCadastroFuncionario(Tela):

    def __init__(self):
        pass

    def init_components(self, alterar=False):

        sg.theme("Reddit")

        dados_funcionario = [
            [sg.Text("Nome:", size=(10, 1)), sg.InputText(key='nome', size=(40, 1))],
            [sg.Text("CPF:", size=(10, 1)), sg.InputText(key='cpf', size=(40, 1))],
            [sg.Text("E-mail:", size=(10, 1)), sg.InputText(key='email', size=(40, 1))],
            [sg.Text("Telefone:", size=(10, 1)), sg.InputText(key='telefone', size=(40, 1))]
        ]

        buttons = [
            [sg.Cancel("Voltar", button_color='gray', key='return', size=(12,1)),
             sg.Submit("Enviar", key='enviar', button_color='green', size=(12,1))]
        ]

        layout = [
                    dados_funcionario,
                    [sg.Text("  ")],
                    [sg.Text("Cargo: (Apenas um)")],
                    
                    [sg.Radio('Operador de caixa', 'cargo', key='operador', enable_events=True, size=(20,1))],
                    [sg.Radio('Supervisor', 'cargo', key='supervisor', enable_events=True, size=(20,1))],
                    [sg.Text("  ")],
                    buttons,
                ] if not alterar else [
                    dados_funcionario,
                    [sg.Text("  ")],
                    buttons,
                ]

        super().__init__(sg.Window("Novo funcionário" if not alterar else "Alterar funcionário", layout=layout, resizable=False, finalize=True), (400, 200 if not alterar else 150))


    def open(self):
        while True:
            botao, dados = super().read()
            if botao == 'enviar':
                try:
                    if dados is not None and '' not in dados.values():
                        try:
                            if not (dados['cpf'] is None):
                                dados['cpf'] = dados['cpf'].replace('.', '').replace('-', '')
                                dados['telefone'] = dados['telefone'].replace('(', '').replace(')', '').replace('-', '')
                                if dados['cpf'].isnumeric() is False or not len(dados['cpf']) == 11:
                                    raise CPFInvalidoException
                                elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', dados['email']):
                                    raise EmailInvalidoException
                                elif dados['nome'].isascii() is False or dados['nome'].isnumeric() is True:
                                    raise NomeInvalidoException
                                elif len(dados['nome']) < 2 or len(dados['nome']) > 15:
                                    raise NomeInvalidoException
                                elif dados['telefone'].isnumeric() is False or (not len(dados['telefone']) >= 6 and len(dados['telefone']) <= 15):
                                    raise TelefoneInvalidoException
                                elif dados['operador'] is False and dados['supervisor'] is False:
                                    raise CargoInvalidoException
                                else:
                                    dados['cargo'] = 'operador' if dados['operador'] else 'supervisor'
                                    #super().close()
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
                        except CargoInvalidoException as c:
                            super().show_message('Cargo inválido!', c)
                    else:
                        raise EntradaVaziaException
                except EntradaVaziaException as g:
                    super().show_message('Campos incompletos!', g)

            elif botao in ('return', sg.WIN_CLOSED):
                super().close()
                break
        return botao, dados

