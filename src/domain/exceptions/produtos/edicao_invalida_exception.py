class EdicaoInvalidaException(Exception):
    def __init__(self):
        super().__init__("\nO campo edição deve conter um valor válido. Ex.: 1.0 ou Edição 1\n")