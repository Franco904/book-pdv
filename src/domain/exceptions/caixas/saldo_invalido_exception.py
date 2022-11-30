class SaldoInvalidoException(Exception):
    def __init__(self):
        super().__init__(f"\nSaldo do caixa deve ser um valor numérico!")
