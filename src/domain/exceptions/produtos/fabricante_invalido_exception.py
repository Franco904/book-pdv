class FabricanteInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nO campo fabricante deve conter entre 2 e 20 caracteres.\n")