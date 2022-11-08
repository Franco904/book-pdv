class AbrirCaixaException(Exception):
    def __init__(self):
        super().__init__("\nOcorreu um erro e o registro de caixa recém-aberto não pode ser salvo.\n")