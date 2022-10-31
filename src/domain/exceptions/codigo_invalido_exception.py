class CodigoInvalidoException(Exception):
    def __init__(self, entidade: str):
        super().__init__(f"\nCódigo de {entidade} inválido!")
