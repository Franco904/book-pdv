class TelefoneInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nDigite um número de Telefone válido:\nO telefone é composto de 6 a 15 números, podendo ou não ser formatado.\n Ex.: (48)91234-1234 ou 48912341234\n")