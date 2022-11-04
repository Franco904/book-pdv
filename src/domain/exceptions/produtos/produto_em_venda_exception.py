class ProdutoEmVendaException(Exception):
    def __init__(self):
        super().__init__("\nO produto não foi removido, pois se encontra em uma venda cadastrada.\n")