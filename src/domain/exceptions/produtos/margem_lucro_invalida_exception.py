class MargemLucroInvalidaException(Exception):
    def __init__(self):
        super().__init__("\nO campo margem de lucro deve conter um valor válido. Ex: 10 ou 5.50\n")