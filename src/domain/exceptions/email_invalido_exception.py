class EmailInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nDigite um e-mail válido.")