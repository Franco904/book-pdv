class DescontoInvalidoException(Exception):
    def __init__(self, entidade: str):
        super().__init__(f"\nDesconto inválido!\n O desconto deve ser de 0% a 100%")
