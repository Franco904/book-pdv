class ExcluirFuncionarioLogadoException(Exception):
    def __init__(self):
        super().__init__(f"\nO funcionário está logado no sistema não pode ser excluído")
