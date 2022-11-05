import PySimpleGUI as sg
from src.data.dao.produto_dao import ProdutoDAO
from src.domain.views.produtos.tela_inicial_produtos import TelaIncialProdutos
from src.domain.views.produtos.tela_cadastrar_produtos import TelaCadastrarProduto
from src.domain.views.produtos.tela_busca_produto import TelaBuscaProduto
from src.domain.views.tela_confirmacao import TelaConfirmacao
from src.domain.views.produtos.tela_desconto import TelaDesconto
from src.domain.enums import PaisEnum
from src.domain.models.livro import Livro
from src.domain.models.eletronico import Eletronico
from src.domain.models.produto import Produto
from src.domain.exceptions.produtos.produto_ja_cadastrado_exception import ProdutoJaCadastradoException
from src.domain.exceptions.produtos.produto_em_venda_exception import ProdutoEmVendaException


class ControladorProdutos:
    def __init__(self, produto_dao: ProdutoDAO) -> None:
        self.__produto_dao = produto_dao
        self.__tela_inicial_produtos = TelaIncialProdutos()
        self.__tela_cadastrar_produtos = TelaCadastrarProduto()
        self.__tela_busca_produto = TelaBuscaProduto()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__tela_desconto = TelaDesconto()

    def get_produtos(self, is_supervisor: bool):
        produtos = self.__produto_dao.get_all()

        if not is_supervisor:
            colunas_livros = ['ID Livro', 'Título', 'Descrição', 'ISBN', 'Autor', 'Edição', 'Editora', 'País',
                              'Preço final']
            colunas_eletronicos = ['ID Eletrônico', 'Título', 'Descrição', 'Fabricante', 'Preço final']

            parsed_livros = [[livro.id_produto,
                              livro.titulo,
                              livro.descricao,
                              livro.isbn,
                              livro.autor,
                              livro.edicao,
                              livro.editora,
                              livro.pais,
                              livro.preco_final] for livro in produtos['livros']]
            parsed_eletronicos = [[eletronico.id_produto,
                                   eletronico.titulo,
                                   eletronico.descricao,
                                   eletronico.fabricante,
                                   eletronico.preco_final] for eletronico in produtos['eletronicos']]
        else:
            colunas_livros = ['ID Livro', 'Título', 'Descrição', 'ISBN', 'Autor', 'Edição', 'Editora', 'País', 'Custo',
                              'Margem Lucro (%)', 'Desconto (%)', 'Preço final']
            colunas_eletronicos = ['ID Eletrônico', 'Título', 'Descrição', 'Fabricante', 'Custo',
                                   'Margem Lucro (%)', 'Desconto (%)', 'Preço final']

            parsed_livros = [[livro.id_produto,
                              livro.titulo,
                              livro.descricao,
                              livro.isbn,
                              livro.autor,
                              livro.edicao,
                              livro.editora,
                              livro.pais,
                              livro.custo,
                              livro.margem_lucro,
                              livro.desconto,
                              livro.preco_final] for livro in produtos['livros']]

            parsed_eletronicos = [[eletronico.id_produto,
                                   eletronico.titulo,
                                   eletronico.descricao,
                                   eletronico.fabricante,
                                   eletronico.custo,
                                   eletronico.margem_lucro,
                                   eletronico.desconto,
                                   eletronico.preco_final] for eletronico in produtos['eletronicos']]

        dados_produtos = {
            'livros': {
                'lista': parsed_livros,
                'colunas': colunas_livros
            },
            'eletronicos': {
                'lista': parsed_eletronicos,
                'colunas': colunas_eletronicos
            }
        }

        return dados_produtos

    def cadastrar_produto(self) -> None:
        paises = [p.value for p in PaisEnum]
        self.__tela_cadastrar_produtos.init_components(paises, editar=False)
        botao_cadastro, valores = self.__tela_cadastrar_produtos.open(editar=False)

        if botao_cadastro == 'enviar':
            if valores is not None:
                try:
                    if self.__produto_dao.get_by_id(valores['id_produto']) is not None:
                        raise ProdutoJaCadastradoException(valores['id_produto'])
                    if valores['livro']:
                        produto = Livro(
                            valores['id_produto'],
                            valores['titulo'],
                            valores['descricao'],
                            valores['custo'],
                            valores['margem_lucro'],
                            valores['autor'],
                            valores['edicao'],
                            valores['editora'],
                            valores['isbn'],
                            valores['pais'],
                        )
                    else:
                        produto = Eletronico(
                            valores['id_produto'],
                            valores['titulo'],
                            valores['descricao'],
                            valores['custo'],
                            valores['margem_lucro'],
                            valores['fabricante'],
                        )
                    self.__produto_dao.persist_entity(produto)
                except ProdutoJaCadastradoException as p:
                    self.__tela_cadastrar_produtos.show_message('Produto já cadastrado!', p)
                finally:
                    self.__tela_cadastrar_produtos.close()

    def aplicar_desconto(self) -> None:
        self.__tela_busca_produto.init_components()
        bota_busca, id_produto = self.__tela_busca_produto.open()
        self.__tela_busca_produto.close()

        if bota_busca == 'buscar' and id_produto is not None:
            produto: Produto = self.__produto_dao.get_by_id(id_produto)

            if produto is None:
                self.__tela_busca_produto.show_message('Produto não encontrado',
                                                       'Não foi encontrado um produto cadastrado com esse ID.')
            else:
                self.__tela_desconto.init_components()
                botao_desconto, valores = self.__tela_desconto.open()

                if botao_desconto == 'salvar' and valores is not None:
                    self.__tela_confirmacao.init_components()
                    botao_confirmacao = self.__tela_confirmacao.open()
                    self.__tela_confirmacao.close()

                    if botao_confirmacao == 'confirmar':
                        if valores['valor_desconto'] != produto.desconto:
                            self.__produto_dao.update_entity(produto.id_produto, 'desconto',
                                                             valores['valor_desconto'])

    def editar_produto(self) -> None:
        self.__tela_busca_produto.init_components()
        botao_busca, id_produto = self.__tela_busca_produto.open()
        self.__tela_busca_produto.close()

        if botao_busca == 'buscar' and id_produto is not None:
            produto: Produto = self.__produto_dao.get_by_id(id_produto)

            if produto is None:
                self.__tela_busca_produto.show_message('Produto não encontrado',
                                                       'Não foi encontrado um produto cadastrado com esse ID.')
            else:
                if produto.id_tipo_produto == 0:
                    tipo_produto = 'livro'
                    dados_produto = {
                        'id_produto': produto.id_produto,
                        'titulo': produto.titulo,
                        'descricao': produto.descricao,
                        'custo': produto.custo,
                        'margem_lucro': produto.margem_lucro,
                        'desconto': produto.desconto,
                        'isbn': produto.isbn,
                        'autor': produto.autor,
                        'edicao': produto.edicao,
                        'editora': produto.editora,
                        'pais': produto.pais,
                        'id_tipo_produto': produto.id_tipo_produto
                    }
                else:
                    tipo_produto = 'eletronico'
                    dados_produto = {
                        'id_produto': produto.id_produto,
                        'titulo': produto.titulo,
                        'descricao': produto.descricao,
                        'custo': produto.custo,
                        'margem_lucro': produto.margem_lucro,
                        'desconto': produto.desconto,
                        'fabricante': produto.fabricante,
                        'pais': produto.pais,
                        'id_tipo_produto': produto.id_tipo_produto
                    }

                paises = [p.value for p in PaisEnum]
                self.__tela_cadastrar_produtos.init_components(paises, editar=True, dados_produto=dados_produto)
                botao_cadastro, dados_novos_produto = self.__tela_cadastrar_produtos.open(editar=True)

                if botao_cadastro == 'enviar':
                    self.__tela_cadastrar_produtos.close()
                    self.__tela_confirmacao.init_components()
                    botao_confirmacao = self.__tela_confirmacao.open()
                    self.__tela_confirmacao.close()

                    inputs = ['titulo', 'descricao', 'custo', 'margem_lucro', 'desconto']

                    if tipo_produto == 'livro':
                        inputs += ['isbn', 'autor', 'edicao', 'editora', 'pais']
                    else:
                        inputs += ['fabricante']

                    if botao_confirmacao == 'confirmar':
                        for element in inputs:
                            if dados_novos_produto[element] != dados_produto[element]:
                                self.__produto_dao.update_entity(dados_produto['id_produto'], element,
                                                                 dados_novos_produto[element])

    def excluir_produto(self) -> None:
        self.__tela_busca_produto.init_components()
        botao_busca, id_produto = self.__tela_busca_produto.open()

        try:
            if botao_busca == 'buscar' and id_produto is not None:
                produto: Produto = self.__produto_dao.get_by_id(id_produto)

                if produto is None:
                    self.__tela_busca_produto.show_message('Produto não encontrado',
                                                           'Não foi encontrado um produto cadastrado com esse ID.')
                    self.__tela_busca_produto.close()
                else:
                    if not self.__produto_dao.has_product_venda(produto.id_produto):
                        self.__tela_busca_produto.close()
                        self.__tela_confirmacao.init_components()
                        botao_confirmacao = self.__tela_confirmacao.open()
                        self.__tela_confirmacao.close()

                        if botao_confirmacao == 'confirmar':
                            self.__produto_dao.delete_entity(produto.id_produto)
                    else:
                        raise ProdutoEmVendaException
        except ProdutoEmVendaException as p:
            self.__tela_busca_produto.show_message('Erro ao excluir', p)
            self.__tela_busca_produto.close()

    def abre_tela(self, is_supervisor: bool):
        opcoes = {'novo': self.cadastrar_produto, 'desconto': self.aplicar_desconto,
                  'editar': self.editar_produto, 'excluir': self.excluir_produto}

        while True:
            dados_produtos = self.get_produtos(is_supervisor)
            self.__tela_inicial_produtos.init_components(dados_produtos['livros'], dados_produtos['eletronicos'],
                                                         is_supervisor)
            opcao_escolhida = self.__tela_inicial_produtos.open()

            if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                self.__tela_inicial_produtos.close()
                break
            else:
                opcoes[opcao_escolhida]()
