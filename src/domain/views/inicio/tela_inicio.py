import PySimpleGUI as sg

from src.domain.views.tela_abstrata import Tela


class TelaInicio(Tela):
    def __init__(self):
        pass

    def init_components(self, nome_funcionario='', is_operador=False):
        cargo_funcionario = 'Operador de caixa' if is_operador else 'Supervisor'

        main_msg = 'Clique no botão abaixo para realizar uma abertura de caixa' if is_operador \
            else 'Clique no botão abaixo para gerenciar funcionários cadastrados'

        sg.theme('Reddit')

        layout = [
            [sg.Text(nome_funcionario, size=(24, 0), font=('', 13))],
            [sg.Text(cargo_funcionario, size=(20, 1))],
        ]

        if is_operador:
            layout.append(
                [
                    [sg.Submit('Caixas', key='caixas', button_color='green', pad=(5, 15)),
                     sg.Text(f"      {main_msg}", size=(48, 1), justification='center')],
                    [sg.Submit('Sair', key='sair', button_color='green'),
                     sg.Push(),
                     sg.Submit('Novo', key='novo', button_color='green')],
                ]
            )
        else:
            layout.append(
                [
                    [sg.Submit('Relatório de vendas', key='relatorio', button_color='green', pad=(5, 15)),
                     sg.Text(f'       {main_msg}', size=(48, 1), justification='center')],
                    [sg.Submit('Produtos', key='produtos', button_color='green'),
                     sg.Push(),
                     sg.Submit('Manejar funcionários', key='funcionarios', button_color='green')],
                    [sg.Submit('Sair', key='sair', button_color='green')],
                ]
            )

        super().__init__(sg.Window('Início', layout=layout, resizable=False, finalize=True), (500, 50))

    def open(self):
        botao, dados = super().read()

        if botao in ('sair', None, sg.WIN_CLOSED):
            super().close()

        super().close()
        return botao

    def close(self):
        super().close()
