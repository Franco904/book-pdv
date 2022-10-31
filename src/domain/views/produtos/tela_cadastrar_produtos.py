from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg


class TelaCadastroProduto(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, paises: list, alterar: bool = False, dados_produto: dict = None) -> None:
        sg.theme("Reddit")

        radio_group = [
            sg.Text('Tipo de produto (Apenas um):'),
            sg.Radio('Livro/Revista/Similar', 'tipo_produto', key='livro', enable_events=True, default=True),
            sg.Radio('Eletronico', 'tipo_produto', key='eletronico', enable_events=True)
        ]

        botoes = [
            [sg.Text('   ')],
            [
                sg.Cancel('Voltar', key='voltar', button_color='gray', size=(20, 1), pad=((30, 20), (0, 0))),
                sg.Submit('Enviar', key='enviar', size=(20, 1), pad=((30, 30), (0, 0)))
            ]
        ]

        atributos_produto = [
            [sg.Text('   ')],
            [
                sg.Text('Título', size=(9, 1)),
                sg.InputText(dados_produto['titulo'] if alterar else '', key='titulo', size=(50, 1))
            ],
            [sg.Text('   ')],
            [sg.Text('Descrição')],
            [sg.Multiline(dados_produto['descricao'] if alterar else '', key='descricao', size=(60, 8))],
            [sg.Text('   ')],
            [
                sg.Text('Custo', size=(12, 1)),
                sg.InputText(dados_produto['custo'] if alterar else '', key='custo', size=(22, 1))
            ],
            [
                sg.Text('Margem Lucro', size=(12, 1)),
                sg.InputText(dados_produto['margem_lucro'] if alterar else '', key='margem_lucro', size=(22, 1))
            ]
        ]

        nome_tela = 'Cadastrar Produto'

        if alterar:
            nome_tela = 'Alterar Produto'
            radio_group = [sg.Text('Alterar dados do produto')]

            if dados_produto['id_tipo_produto'] == 0:
                atributos_produto.append([
                    [
                        sg.Text('Desconto', size=(12, 1)),
                        sg.InputText(dados_produto['desconto'] if alterar else '', key='desconto', size=(22, 1))
                    ],
                    [
                        sg.Text('ISBN', key='isbn_text', size=(12, 1)),
                        sg.InputText(dados_produto['isbn'] if alterar else '', key='isbn', size=(22, 1)),
                    ],
                    [
                        sg.Text('Autor', key='autor_text', size=(12, 1)),
                        sg.InputText(dados_produto['autor'] if alterar else dados_produto[''] if alterar else '',
                                     key='autor', size=(22, 1))
                    ],
                    [
                        sg.Text('Edição', key='edicao_text', size=(12, 1)),
                        sg.InputText(dados_produto['edicao'] if alterar else '', key='edicao', size=(22, 1))
                    ],
                    [
                        sg.Text('Editora', key='editora_text', size=(12, 1)),
                        sg.InputText(dados_produto['editora'] if alterar else '', key='editora', size=(22, 1))
                    ],
                    [
                        sg.Text('País', key='pais_text', size=(12, 1)),
                        sg.Combo(paises, enable_events=True, readonly=True, size=(20, 1),
                                 key='pais', default_value=dados_produto['pais'] if alterar else '')
                    ],
                ])
            else:
                atributos_produto.append([
                    [
                        sg.Text('Desconto', size=(12, 1)),
                        sg.InputText(dados_produto['desconto'] if alterar else '', key='desconto', size=(22, 1))
                    ],
                    [
                        sg.Text('Fabricante', size=(12, 1), key='fabricante_text', visible=False),
                        sg.InputText(dados_produto['fabricante'] if alterar else '',
                                     key='fabricante', size=(22, 1), visible=False)
                    ]
                ])
        else:
            atributos_produto.append([
                [
                    sg.Text('ISBN', key='isbn_text', size=(12, 1)),
                    sg.InputText(key='isbn', size=(22, 1)),

                    sg.Text('Fabricante', size=(12, 1), key='fabricante_text', visible=False),
                    sg.InputText(key='fabricante', size=(22, 1), visible=False)
                ],
                [
                    sg.Text('Autor', key='autor_text', size=(12, 1)),
                    sg.InputText(key='autor', size=(22, 1))
                ],
                [
                    sg.Text('Edição', key='edicao_text', size=(12, 1)),
                    sg.InputText(key='edicao', size=(22, 1))
                ],
                [
                    sg.Text('Editora', key='editora_text', size=(12, 1)),
                    sg.InputText(key='editora', size=(22, 1))
                ],
                [
                    sg.Text('País', key='pais_text', size=(12, 1)),
                    sg.Combo(paises, enable_events=True, readonly=True, size=(20, 1), key='pais')
                ],
            ])

        layout = [
            radio_group,
            atributos_produto,
            botoes
        ]

        super().__init__(sg.Window(nome_tela, layout=layout, resizable=False, modal=True, finalize=True))

    def open(self, alterar: bool = False) -> tuple:

        def alternar_atributos_produto(window, evento_tela):
            elementos_livro = [
                'isbn_text',
                'isbn',
                'autor_text',
                'autor',
                'edicao_text',
                'edicao',
                'editora_text',
                'editora',
                'pais_text',
                'pais'
            ]
            if evento_tela == 'livro' and evento_tela:
                window['fabricante'].update(visible=False)
                window['fabricante_text'].update(visible=False)
                for elemento in elementos_livro:
                    window[elemento].update(visible=True)

            if evento_tela == 'eletronico' and evento_tela:
                window['fabricante_text'].update(visible=True)
                window['fabricante'].update(visible=True)

                for elemento in elementos_livro:
                    window[elemento].update(visible=False)

        while True:
            evento, valores = super().read()

            alternar_atributos_produto(super().window, evento)

            if evento == 'enviar':
                print(valores)
                """
                    TODO: input validation cases
                """

            if evento is None or evento == sg.WIN_CLOSED or evento == 'voltar':
                super().close()
                break

        return evento, valores
