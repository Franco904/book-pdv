class VendaNaoEncontradaException(Exception):
    def __init__(self):
        super().__init__("\nNão foi encontrada uma venda cadastrada com esse ID.\n")
