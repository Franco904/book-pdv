from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg
from src.domain.exceptions.senha_invalida_exception import SenhaInvalidaException
from src.domain.exceptions.senhas_diferentes_exception import SenhasDiferentesException
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.exceptions.senha_nova_igual_atual_exception import SenhaNovaIgualAtualException


class TelaCadastrarSenha(Tela):
    def __init__(self):
        pass

    def init_components(self, editando=False):
        sg.theme('Reddit')
        layout = [
            [sg.Text('  ')],
            [sg.Text('Senha atual:', size=(10, 1), visible=editando),
             sg.InputText(key='senha_atual', size=(40, 1), visible=editando)],
            [sg.Text('  ', visible=editando)],
            [sg.Text('Nova senha:', size=(10, 1)), sg.InputText(key='senha_nova', size=(40, 1))],
            [sg.Text('Repetir senha:', size=(10, 1)), sg.InputText(key='repetir_senha', size=(40, 1))],
            [sg.Cancel('Voltar', key='voltar', button_color='gray', size=(12, 1))],
            [sg.Cancel('Salvar', key='salvar', button_color='green', size=(12, 1))]
        ]

        super().__init__(
            sg.Window('Nova senha', layout=layout, resizable=False, modal=True, finalize=True,
                      element_justification='c'), (200, 100))

    def open(self, editando=False):
        while True:
            botao, dados = super().read()
            try:
                if botao == 'salvar':
                    if not editando:
                        if '' in (dados['senha_nova'], dados['repetir_senha']):
                            raise EntradaVaziaException

                        if not dados['senha_nova'].isalnum() or 6 >= len(dados['senha_nova']) >= 18:
                            raise SenhaInvalidaException

                        elif dados['senha_nova'] != dados['repetir_senha']:
                            raise SenhasDiferentesException

                        else:
                            super().close()
                            break
                    else:
                        if '' in dados.values():
                            raise EntradaVaziaException

                        if not dados['senha_atual'].isalnum() or 6 >= len(dados['senha_nova']) >= 18 \
                                or not dados['senha_nova'].isalnum() or 6 >= len(dados['senha_nova']) >= 18:
                            raise SenhaInvalidaException

                        elif dados['senha_atual'] == dados['senha_nova']:
                            raise SenhaNovaIgualAtualException

                        elif dados['senha_nova'] != dados['repetir_senha']:
                            raise SenhasDiferentesException

                        else:
                            # super().close()
                            break
                if botao in ('voltar', None, sg.WIN_CLOSED):
                    super().close()
                    break
            except EntradaVaziaException as e:
                super().show_message('Campos incompletos', e)
            except SenhaInvalidaException as s:
                super().show_message('Senha inválida', s)
            except SenhasDiferentesException as p:
                super().show_message('Senhas diferentes', p)
            except SenhaNovaIgualAtualException as q:
                super().show_message('Senhas nova e atual iguais', q)

        return botao, dados
