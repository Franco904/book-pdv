import PySimpleGUI as sg

from src.domain.views.tela_abstrata import Tela


class TelaInicio(Tela):
    def __init__(self):
        pass

    def init_components(self, isOperador = False):
        nomeFuncionario = "Carlos Alberto Sampaio"
        cargoFuncionario = "Operador de caixa"

        btnOptions = {
            "main": "Novo" if isOperador else "Manejar funcionários",
            "first": "Histórico de caixas" if isOperador else "Relatórios de vendas",
            "second": "Produtos",
            "third": "Sair"
        }

        sg.theme("Reddit")
        layout = [
            [sg.Text(nomeFuncionario, size=(24, 0), font=('', 13))],
            [sg.Text(cargoFuncionario, size=(20, 1))],

            [sg.Submit(btnOptions["first"], key="1", button_color='green', pad=(5, 15)),
             sg.Text("       Clique no botão abaixo para realizar uma abertura de caixa", size=(48, 1),
                     justification='center')],
            [sg.Submit(btnOptions["second"] if not isOperador else btnOptions["third"],
                       key="2", button_color='green'),
             sg.Text("                                                                  "),
             sg.Submit(btnOptions["main"], key="3", button_color='green')],
            [sg.Submit(btnOptions["third"], key="4", button_color='green', visible=not isOperador)],
        ]

        super().__init__(sg.Window("Início", layout=layout, resizable=False, finalize=True), (500, 50))

    def open(self):
        option = -1
        while option == -1:
            button, values = super().read()

            if button in ("0", None, sg.WIN_CLOSED):
                option = 0
                break

            option = int(button)
            super().close()

        super().close()
        return option

    def close(self):
        super().close()
