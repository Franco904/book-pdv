class ListaVaziaException(Exception):
    def __init__(self,):
        super().__init__(f"\nNão foram encontradas observações na tabela.\n")