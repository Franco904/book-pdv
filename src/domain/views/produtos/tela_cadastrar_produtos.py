from src.domain.views.tela_abstrata import Tela
import PySimpleGUI as sg
from src.domain.exceptions.entrada_vazia_exception import EntradaVaziaException
from src.domain.exceptions.produtos.titulo_invalido_exception import TituloInvalidoException
from src.domain.exceptions.produtos.descricao_invalida_exception import DescricaoInvalidaException
from src.domain.exceptions.produtos.custo_invalido_exception import CustoInvalidoException
from src.domain.exceptions.produtos.margem_lucro_invalida_exception import MargemLucroInvalidaException
from src.domain.exceptions.produtos.desconto_invalido_exception import DescontoInvalidoException
from src.domain.exceptions.produtos.isbn_invalido_exception import ISBNInvalidoException
from src.domain.exceptions.produtos.autor_invalido_exception import AutorInvalidoException
from src.domain.exceptions.produtos.edicao_invalida_exception import EdicaoInvalidaException
from src.domain.exceptions.produtos.editora_invalida_exception import EditoraInvalidaException
from src.domain.exceptions.produtos.fabricante_invalido_exception import FabricanteInvalidoException
from src.domain.exceptions.produtos.produto_invalido_exception import ProdutoInvalidoException
from src.domain.exceptions.produtos.id_invalido_exception import IDInvalidoException


class TelaCadastrarProduto(Tela):
    def __init__(self) -> None:
        pass

    def init_components(self, paises: list, editar: bool = False, dados_produto: dict = None) -> None:
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
                sg.Text('ID produto', key='id_produto_text', size=(9, 1)),
                sg.InputText(dados_produto['id_produto'] if editar else '', key='id_produto', size=(50, 1))
            ] if not editar else [],
            [
                sg.Text('Título', size=(9, 1)),
                sg.InputText(dados_produto['titulo'] if editar else '', key='titulo', size=(50, 1))
            ],
            [sg.Text('   ')],
            [sg.Text('Descrição')],
            [sg.Multiline(dados_produto['descricao'] if editar else '', key='descricao', size=(60, 8))],
            [sg.Text('   ')],
            [
                sg.Text('Custo', size=(12, 1)),
                sg.InputText(dados_produto['custo'] if editar else '', key='custo', size=(22, 1))
            ],
            [
                sg.Text('Margem Lucro', size=(12, 1)),
                sg.InputText(dados_produto['margem_lucro'] if editar else '', key='margem_lucro', size=(22, 1))
            ]
        ]

        nome_tela = 'Cadastrar Produto'

        if editar:
            nome_tela = 'Editar Produto'
            radio_group = [sg.Text('Editar dados do produto')]

            if dados_produto['id_tipo_produto'] == 0:
                atributos_produto.append([
                    [
                        sg.Text('Desconto', size=(12, 1)),
                        sg.InputText(dados_produto['desconto'] if editar else '', key='desconto', size=(22, 1))
                    ],
                    [
                        sg.Text('ISBN', key='isbn_text', size=(12, 1)),
                        sg.InputText(dados_produto['isbn'] if editar else '', key='isbn', size=(22, 1)),
                    ],
                    [
                        sg.Text('Autor', key='autor_text', size=(12, 1)),
                        sg.InputText(dados_produto['autor'] if editar else dados_produto[''] if editar else '',
                                     key='autor', size=(22, 1))
                    ],
                    [
                        sg.Text('Edição', key='edicao_text', size=(12, 1)),
                        sg.InputText(dados_produto['edicao'] if editar else '', key='edicao', size=(22, 1))
                    ],
                    [
                        sg.Text('Editora', key='editora_text', size=(12, 1)),
                        sg.InputText(dados_produto['editora'] if editar else '', key='editora', size=(22, 1))
                    ],
                    [
                        sg.Text('País', key='pais_text', size=(12, 1)),
                        sg.Combo(paises, enable_events=True, readonly=True, size=(20, 1),
                                 key='pais', default_value=dados_produto['pais'] if editar else '')
                    ],
                ])
            else:
                atributos_produto.append([
                    [
                        sg.Text('Desconto', size=(12, 1)),
                        sg.InputText(dados_produto['desconto'] if editar else '', key='desconto', size=(22, 1))
                    ],
                    [
                        sg.Text('Fabricante', size=(12, 1), key='fabricante_text'),
                        sg.InputText(dados_produto['fabricante'] if editar else '',
                                     key='fabricante', size=(22, 1))
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

    def open(self, editar: bool = False) -> tuple:

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

        def validate_numeric_input(key: str):
            try:
                if '.' not in dados[key]:
                    dados[key] = int(dados[key])
                else:
                    dados[key] = float(dados[key])
                return True
            except ValueError:
                return False

        def validate_id_produto_input():
            if not validate_numeric_input('id_produto'):
                raise IDInvalidoException

        def validate_common_inputs():
            if dados['titulo'].isnumeric() is True or len(dados['titulo']) < 2 or len(dados['titulo']) > 20:
                raise TituloInvalidoException
            elif dados['descricao'].isnumeric() is True or len(dados['descricao']) < 2 or len(dados['descricao']) > 50:
                raise DescricaoInvalidaException
            elif not validate_numeric_input('custo'):
                raise CustoInvalidoException
            elif not validate_numeric_input('margem_lucro'):
                raise MargemLucroInvalidaException

        def validate_desconto_input():
            if not validate_numeric_input('desconto') or dados['desconto'] < 0 or dados['desconto'] > 100:
                raise DescontoInvalidoException

        def validate_livro_input():
            if '-' in dados['isbn']:
                if len(dados['isbn']) != 17:
                    raise ISBNInvalidoException
            elif dados['isbn'].replace('-', '').isnumeric() is False or len(dados['isbn'].replace('-', '')) != 13:
                raise ISBNInvalidoException
            elif dados['autor'].isnumeric() is True or len(dados['autor']) < 2 or len(dados['autor']) > 20:
                raise AutorInvalidoException
            elif dados['edicao'].isascii() is False or len(dados['edicao']) < 1 or len(dados['edicao']) > 20:
                raise EdicaoInvalidaException
            elif dados['editora'].isnumeric() is True or len(dados['editora']) < 2 or len(dados['editora']) > 20:
                raise EditoraInvalidaException

        def validate_eletronico_input():
            if dados['fabricante'].isnumeric() is True or len(dados['fabricante']) < 2 or len(dados['fabricante']) > 20:
                raise FabricanteInvalidoException

        def validate_new_product(product_type_validation):
            validate_id_produto_input()
            validate_common_inputs()
            product_type_validation()

        def validate_update_product(product_type_validation):
            validate_common_inputs()
            validate_desconto_input()
            product_type_validation()

        def check_if_livro():
            try:
                isbn_check = dados['isbn']
                is_livro = True
            except KeyError:
                is_livro = False

            return is_livro

        def validate_all_inputs():
            common_inputs = [
                dados['titulo'],
                dados['descricao'],
                dados['custo'],
                dados['margem_lucro']
            ]

            if not editar:
                if not all([dados['livro'], dados['eletronico']]):
                    if dados['livro']:
                        inputs_new_livro = [
                            dados['id_produto'],
                            dados['isbn'],
                            dados['autor'],
                            dados['edicao'],
                            dados['editora'],
                            dados['pais']
                        ]
                        if '' in common_inputs + inputs_new_livro:
                            raise EntradaVaziaException

                        validate_new_product(validate_livro_input)

                    if dados['eletronico']:
                        inputs_eletronico = [
                            dados['id_produto'],
                            dados['fabricante']
                        ]
                        if '' in common_inputs + inputs_eletronico:
                            raise EntradaVaziaException

                        validate_new_product(validate_eletronico_input)
                else:
                    raise ProdutoInvalidoException
            else:
                input_desconto = [
                    dados['desconto']
                ]

                is_livro = check_if_livro()

                if is_livro:
                    inputs_update_livro = [
                        dados['isbn'],
                        dados['autor'],
                        dados['edicao'],
                        dados['editora'],
                        dados['pais']
                    ]
                    if '' in common_inputs + inputs_update_livro + input_desconto:
                        raise EntradaVaziaException

                    validate_update_product(validate_livro_input)

                else:
                    if '' in common_inputs + [dados['fabricante']] + input_desconto:
                        raise EntradaVaziaException

                    validate_update_product(validate_eletronico_input)

        while True:
            evento, dados = super().read()

            alternar_atributos_produto(super().window, evento)

            if evento == 'enviar':
                try:
                    validate_all_inputs()
                    break
                except EntradaVaziaException as a:
                    super().show_message('Campos incompletos!', a)
                except TituloInvalidoException as b:
                    super().show_message('Título inválido!', b)
                except DescricaoInvalidaException as c:
                    super().show_message('Descrição inválida!', c)
                except CustoInvalidoException as d:
                    super().show_message('Custo inválido!', d)
                except MargemLucroInvalidaException as e:
                    super().show_message('Margem de lucro inválida!', e)
                except DescontoInvalidoException as f:
                    super().show_message('Desconto inválido!', f)
                except ISBNInvalidoException as g:
                    super().show_message('ISBN inválido!', g)
                except AutorInvalidoException as h:
                    super().show_message('Autor inválido!', h)
                except EdicaoInvalidaException as i:
                    super().show_message('Edição inválida!', i)
                except EditoraInvalidaException as j:
                    super().show_message('Editora inválida!', j)
                except FabricanteInvalidoException as k:
                    super().show_message('Fabricante inválido!', k)
                except ProdutoInvalidoException as p:
                    super().show_message('Produto inválido!', p)

            if evento is None or evento == sg.WIN_CLOSED or evento == 'voltar':
                super().close()
                break

        return evento, dados
