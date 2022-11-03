class ProdutoJaCadastradoException(Exception):
    def __init__(self, id_produto: int):
        super().__init__(f"\nO produto {id_produto} já esta cadastrado!")
