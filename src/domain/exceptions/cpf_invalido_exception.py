class CPFInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nDigite um CPF valido:\nO CPF é composto por 11 números, podendo ou não ser formatado.\n Ex.: 123.123.123-12 ou 12312312312\n")