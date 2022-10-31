from src.domain.models.produto import Produto


class Eletronico(Produto):
    def __init__(self,
                 id_tipo_produto: int,
                 titulo: str,
                 descricao: str,
                 custo: float,
                 margem_lucro: float,
                 fabricante: str,
                 desconto: float,
                 autor: str = '',
                 edicao: str = '',
                 editora: str = '',
                 isbn: str = '',
                 pais: str = '',
                 ):
        super().__init__(
            id_tipo_produto,
            titulo,
            descricao,
            custo,
            margem_lucro,
            fabricante,
            autor,
            edicao,
            editora,
            isbn,
            pais,
            desconto
        )
