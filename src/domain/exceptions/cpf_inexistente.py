class CPFInexistenteException(Exception):
    def __init__(self):
        super().__init__("\nO CPF digitado não foi encontrado.\n")