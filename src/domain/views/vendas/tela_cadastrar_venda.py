from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg

class TelaCadastroVenda(Tela):

    def __init__(self) -> None:
        pass

    def init_components(self, alterar: bool = False, data_venda = None,
                        total_venda= None, codigo=None, valor_troco = None, observacoes = None,
                        product_list =None, head_list=None) -> None:
        sg.theme("Reddit")

        data_e_troco = [
            [sg.Text('   ')],
            [sg.Text('Data'),
             sg.Text(data_venda),
             sg.Text('Valor de Troco'),
             sg.InputText(valor_troco, key='troco', size=(22, 1))

             ]
        ]

        codigo_venda = [
            [sg.Text('   ')],
            [sg.Text('Código da Venda'),
             sg.InputText(codigo, key='codigo_venda', size=(22, 1))]
        ]

        total_e_observacoes = [
            [sg.Text('   ')],
            [sg.Text('Total'),
             sg.Text(f'R$ {total_venda}'),
             sg.Text('Observações')],
            [sg.Multiline(observacoes, key='observacoes', size=(60, 8))]
        ]



        buttons= [
            [
                sg.Cancel("Descartar", key='descartar', button_color='gray', size=(9, 1)),
                sg.Submit("Salvar alterações" if alterar else 'Finalizar venda', key='salvar', size=(20, 1)),
                sg.Submit("Incluir produto", key='incluir', size=(20, 1))
            ]


        ]





        nome_tela = 'Nova Venda'

        if alterar:
            nome_tela = 'Alterar venda'

        else:
            pass


        layout =[
            [data_e_troco,
             codigo_venda,
             total_e_observacoes,
             buttons
             ]

        ]

        super().__init__(sg.Window(nome_tela, layout=layout, resizable=False, modal=True, finalize=True,
                                   element_justification='c'), (300, 180))


    def open(self, alterar: bool = False) -> str:
        while True:
            botao, valores = super().read()
            if botao is None or botao == sg.WIN_CLOSED or botao == 'voltar':
                super().close()
                break

            return botao

tela = TelaCadastroVenda()
tela.init_components(data_venda= '04/9/2022', total_venda=245, product_list=[1,2,3], alterar=True)
button, values = tela.open()