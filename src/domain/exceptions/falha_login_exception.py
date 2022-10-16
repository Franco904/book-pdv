class FalhaLoginException(Exception):
    def __init__(self):
        super().__init__(f"\nCredenciais inválidas.")
