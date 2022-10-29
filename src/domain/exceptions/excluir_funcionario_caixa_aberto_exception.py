class ExcluirFuncionarioCaixaAbertoException(Exception):
    def __init__(self):
        super().__init__(f"\nEste funcionário possui caixas abertos no sistema e não pode ser excluído")
