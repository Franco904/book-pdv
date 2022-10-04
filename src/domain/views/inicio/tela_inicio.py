import PySimpleGUI as sg

from src.domain.views.tela_abstrata import Tela


class TelaInicio(Tela):
    def __init__(self):
        pass

    def init_components(self, is_operador = False):
        nomeFuncionario = "Carlos Alberto Sampaio"
        cargoFuncionario = "Operador de caixa"

        btnOptions = {
            "main": "Novo" if is_operador else "Manejar funcionários",
            "first": "Histórico de caixas" if is_operador else "Relatórios de vendas",
            "second": "Produtos",
            "third": "Sair"
        }

        mainMsg = "Clique no botão abaixo para realizar uma abertura de caixa" if is_operador else "Clique no botão abaixo para gerenciar funcionários cadastrados"

        sg.theme("Reddit")
        layout = [
            [sg.Text(nomeFuncionario, size=(24, 0), font=('', 13))],
            [sg.Text(cargoFuncionario, size=(20, 1))],

            [sg.Submit(btnOptions["first"], key="1", button_color='green', pad=(5, 15)),
             sg.Text(f"       {mainMsg}", size=(48, 1),
                     justification='center')],
            [sg.Submit(btnOptions["second"] if not is_operador else btnOptions["third"],
                       key="2", button_color='green'),
             sg.Push(),
             sg.Submit(btnOptions["main"], key="3", button_color='green')],
            [sg.Submit(btnOptions["third"], key="4", button_color='green', visible=not is_operador)],
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
