from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.exceptions.quantidade_invalida_exception import QuantidadeInvalidaException
from src.domain.views.shared.tela_abstrata import Tela
import PySimpleGUI as sg

class TelaIncluirProduto(Tela):

    def __init__(self) -> None:
        pass

    def init_components(self, produtos = None) -> None:
        sg.theme("Reddit")
        layout = [
            [sg.Combo(produtos, key='produtos', size=(20, 1))],
            [
                sg.Text("Quantidade", size=(8, 0), font=('', 10)),
                sg.InputText(key='quantidade', size=(22, 1))
            ],
            [
             sg.Cancel("Voltar", key='voltar', button_color='gray', size=(9, 1)),
             sg.Submit("Incluir", key='incluir', size=(20, 1))
             ]

        ]

        super().__init__(sg.Window("Incluir Produto", layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 80))


    def open(self) -> str:
        while True:
            botao, valores = super().read()
            if botao == 'incluir':
                try:
                    if not valores['quantidade'] == '':
                        if valores['quantidade'].isnumeric() == False:
                            raise QuantidadeInvalidaException
                        valores['quantidade'] = int(valores['quantidade'])
                        break
                    else:
                        raise EntradaVaziaException()

                except EntradaVaziaException as e:
                    super().show_message("Digite um código para buscar!", e)
                except QuantidadeInvalidaException as q:
                    super().show_message("Código Inválido!", q)

            if botao is None or botao == sg.WIN_CLOSED or botao == 'voltar':
                super().close()
                break

            return botao

# tela = TelaIncluirProduto()
# tela.init_components(quantidade='', produtos='')
# button, values = tela.open()