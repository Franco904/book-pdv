from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
import pandas as pd
import sqlalchemy as db

class FuncionarioDAO (AbstractDAO):
    def __init__(self, database: Database):
        super().__init__(database, 'access_control', 'funcionarios')#cache?
        self.__database = database


    def execute_query(self, query: str):
        super().execute_query(query)

test = FuncionarioDAO(Database())
test.execute_query("SELECT * FROM access_control.funcionarios")




