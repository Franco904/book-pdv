class EditoraInvalidaException(Exception):
    def __init__(self):
        super().__init__("\nO campo editora deve conter entre 2 e 20 caracteres.\n")