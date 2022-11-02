class DescontoInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nO campo desconto deve conter um valor válido. Ex: 10 ou 5.50\n")