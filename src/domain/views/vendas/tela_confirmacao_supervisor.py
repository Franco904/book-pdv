from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg

class TelaConfirmacaoSupervisor(Tela):

    def __init__(self) -> None:
        pass

    def init_components(self, senha) -> None:
        sg.theme("Reddit")
        layout = [
            [sg.Text("A operação necessita autorização especial.")],
            [sg.Text("Insira a senha de acesso e, em caso de")],
            [sg.Text("dúvidas, contate o seu supervisor.")],
            [sg.InputText(senha, key='senha', size=(22, 1))],
            [
                sg.Cancel("Voltar", key='voltar', button_color='gray', size=(9, 1)),
                sg.Submit("Enviar", key='enviar', button_color='green', size=(9, 1))
            ]

        ]

        super().__init__(sg.Window("Confirmação do supervisor", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 180))


    def open(self) -> str:
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'voltar':
                super().close()
                break

            return botao


#Remover depois
# tela = TelaConfirmacaoSupervisor()
# tela.init_components('1234123')
# button, values = tela.open()