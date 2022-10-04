import PySimpleGUI as sg

from src.domain.views.tela_abstrata import Tela


class TelaAbrirCaixa(Tela):
    def __init__(self):
        pass

    def init_components(self, caixas_names=None):
        if caixas_names is None:
            return

        data = "19/03/2022"
        valor = "32,59"

        sg.theme("Reddit")
        layout = [
            [sg.Combo(caixas_names, readonly=True, size=(40, 1), key="nome_caixa")],

            [sg.Text("Data", size=(24, 0), font=("", 10)), sg.Text(data, size=(24, 0), font=("", 10), key="data_abertura")],
            [sg.Text("Valor", size=(24, 0), font=("", 10)), sg.Text(valor, size=(24, 0), font=("", 10), key="saldo_abertura")],
            [sg.Text("Observações", size=(24, 0), font=("", 10))],
            [sg.Multiline(size=(50, 5), pad=(5, 5), key="observacoes_field")],
            [sg.Push(), sg.Cancel("Voltar", key="0", button_color="gray"),
             sg.Cancel('Abrir caixa', key="1", button_color="green")]
        ]

        super().__init__(sg.Window("Abrir caixa", layout=layout, resizable=False, finalize=True))

    def open(self):
        option = -1
        values = {}

        while option == -1:
            button, values = super().read()

            if button in ("0", None, sg.WIN_CLOSED):
                option = 0
                break

            elif button == "1":
                if values["nome_caixa"] == "":
                    super().show_message("Atenção!", "Preencha o campo Caixa corretamente!")
                    continue

                option = int(button)
                break

        super().close()
        return option, values

    def close(self):
        super().close()
