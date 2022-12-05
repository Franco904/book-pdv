class CaixaAtivoNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("\nNão foi encontrado um caixa ativo com esse ID.\n")
