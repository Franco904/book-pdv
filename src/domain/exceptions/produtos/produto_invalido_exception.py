class ProdutoInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nO campo tipo de produto deve deve ser preenchido, selecionando uma das duas opções.\n")