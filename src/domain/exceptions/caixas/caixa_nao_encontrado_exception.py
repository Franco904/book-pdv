class CaixaNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("\nNão foi encontrado um caixa com esse ID.\n")
