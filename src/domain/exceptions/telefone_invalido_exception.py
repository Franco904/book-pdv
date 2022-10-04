class TelefoneInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nDigite um número de Telefone válido:\nO telefone é composto por 11 números, podendo ou não ser formatado.\n Ex.: (48)91234-1234 ou 48912341234\n")