from ..tela_abstrata import Tela
import PySimpleGUI as sg

class TelaCadastroVenda(Tela):

    def __init__(self) -> None:
        pass

    def init_components(self, alterar: bool = False, data_venda = None,
                        total_venda= None, codigo=None) -> None:
        sg.theme("Reddit")

        data = [
            [sg.Text('   ')],
            [sg.Text('Data'),
             sg.Text(data_venda)
             ]
        ]

        total = [
            [sg.Text('   ')],
            [sg.Text('Total')],
            [sg.Text(total_venda)]
        ]

        codigo_venda = [
            [sg.Text('   ')],
            [sg.Text('Código da Venda'),
             sg.InputText(codigo, key='codigo_venda', size=(22, 1))]
        ]

        nome_tela = 'Nova Venda'

        if alterar:
            nome_tela = 'Alterar venda'

        else:
            pass


        layout = [

        ]

        super().__init__(sg.Window(nome_tela, layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 180))


    def open(self) -> str:
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'voltar':
                super().close()
                break

            return botao