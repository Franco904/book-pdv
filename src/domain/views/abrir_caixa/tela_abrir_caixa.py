import PySimpleGUI as sg

from src.domain.views.tela_abstrata import Tela


class TelaAbrirCaixa(Tela):
    def __init__(self):
        pass

    def init_components(self, caixas_ids=None, data_abertura=None):
        if caixas_ids is None or data_abertura is None:
            return

        sg.theme("Reddit")
        layout = [
            [sg.Combo(caixas_ids, enable_events=True, readonly=True, size=(40, 1), key="caixa_id")],

            [sg.Text("Data", size=(24, 0), font=("", 10)), sg.Text(data_abertura, size=(24, 0), font=("", 10), key="data_abertura")],
            [sg.Text("Valor", size=(24, 0), font=("", 10)), sg.Text('9', size=(24, 0), font=("", 10), key="saldo_abertura")],
            [sg.Text("Observações", size=(24, 0), font=("", 10))],
            [sg.Multiline(size=(50, 5), pad=(5, 5), key="observacoes")],
            [sg.Push(), sg.Cancel("Voltar", key="0", button_color="gray"),
             sg.Cancel('Abrir caixa', key="1", button_color="green")]
        ]

        super().__init__(sg.Window("Abrir caixa", layout=layout, resizable=False, finalize=True))

    def open(self, caixas: list):
        option = -1

        values = {}
        saldo_abertura = 0

        while option == -1:
            event, values = super().read()

            # Retorno
            if event in ("0", None, sg.WIN_CLOSED):
                option = 0
                break

            # Atualiza dinamicamente o valor de saldo, conforme seleção no combo de caixas
            elif event == "caixa_id":
                id = values["caixa_id"]
                saldo = list(filter(lambda caixa: caixa.id == id, caixas))[0].saldo

                super().update("saldo_abertura", saldo)
                saldo_abertura = saldo

            # Abrir abrir_caixa
            elif event == "1":
                if values["caixa_id"] == "":
                    super().show_message("Atenção!", "Preencha o campo Caixa corretamente!")
                    continue

                option = int(event)
                break

        super().close()
        return {"option": option, "values": values, "saldo_abertura": saldo_abertura}

    def close(self):
        super().close()
