class SangriaInvalidaException(Exception):
    def __init__(self):
        super().__init__(f"\nValor de sangria inválido! O valor deve ser maior ou igual a 0 e não deve exceder o "
                         f"valor total presente no caixa.")
