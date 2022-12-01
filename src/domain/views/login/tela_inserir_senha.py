from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaInserirSenha(Tela):
    def __init__(self):
        pass

    def init_components(self):
        sg.theme('Reddit')
        layout = [
                    [sg.Text('  ')],
                    [sg.Text('Senha:', size=(10, 1))],
                    [sg.InputText(key='senha', size=(40, 1))],
                    [sg.Text('Alterar senha', key='alterar_senha', size=(10, 1), enable_events=True, text_color='green')],
                    [sg.Cancel('Voltar', key='voltar', button_color='gray', size=(12, 1))],
                    [sg.Cancel('Login', key='login', button_color='green', size=(12, 1))]
                  ]

        super().__init__(
            sg.Window('Inserir senha', layout=layout, resizable=False, modal=True, finalize=True, element_justification='c'), (200, 100))

    def open(self):
        while True:
            evento, dados = super().read()
            try:
                if evento == 'login':
                    if dados['senha'] == '':
                        raise EntradaVaziaException
                    else:
                        super().close()
                        break

                if evento == 'alterar_senha' or evento in ('voltar', None, sg.WIN_CLOSED):
                    super().close()
                    break

            except EntradaVaziaException as e:
                super().show_message('Campo incompleto!', e)

        return evento, dados
