import PySimpleGUI as sg

from src.domain.views.shared.tela_abstrata import Tela


class TelaPainelCaixa(Tela):
    def __init__(self):
        pass

    def init_components(self, nome_operador='', id_caixa='') -> None:
        sg.theme("Reddit")
        layout = [
            [sg.Text(nome_operador, size=(24, 0), font=('', 13))],
            [sg.Text('Operador de caixa', size=(20, 1))],
            [sg.Text('                 ', size=(20, 1))],
            [sg.Push()],
            [sg.Text('Código do caixa', size=(24, 0), font=('', 13))],
            [sg.Text(id_caixa, size=(20, 1))],

            [sg.Submit("Cadastro de vendas", key='vendas', size=(20, 1))],
            [sg.Submit("Registro de sangrias", key='sangrias', size=(20, 1))],
            [sg.Submit("Ver movimentações", key='movimentacoes', size=(20, 1))],
            [sg.Cancel('Fechar caixa', key='fechar_caixa', button_color='green', size=(12, 1))],
            [sg.Text('                 ', size=(20, 1))],
        ]

        super().__init__(sg.Window("Painel do caixa", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 180))

    def open(self, nome_operador='', id_caixa='') -> str:
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'voltar':
                super().show_message('Atenção!', 'É necessário fechar o caixa antes de retornar!')
                self.init_components(nome_operador, id_caixa)
                continue

            else:
                super().close()
                break

        return botao

    def close(self) -> None:
        super().close()
