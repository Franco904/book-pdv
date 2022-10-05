from sqlalchemy import create_engine
import sqlalchemy as db
import pandas as pd

class Database:
    def __init__(self):
        self.__hostname = "54.147.36.107"
        self.__database = "dfb5983k0abcf8"
        self.__username = "rusdkrqlyrnzgx"
        self.__password = "a7b9f182a0e99bf63b4f19c63eee7db3aa5691840897684266ee56796e9d74f8"
        self.__port = 5432
        self.__engine = self.create_db_engine()
        self.__metadata = db.MetaData()

    def create_db_engine(self):
        postgres_engine = create_engine(f"postgresql://{self.__username}:{self.__password}"
                                        f"@{self.__hostname}:{self.__port}/{self.__database}")
        return postgres_engine

    @property
    def engine(self):
        return self.__engine

    @property
    def metadata(self):
        return self.__metadata

    def open_connection(self):
        print("Conexão aberta com sucesso")
        return self.__engine.connect()

    def close_db(self):
        print("Conexão fechada com sucesso")
        return self.__engine.dispose()

"""
test = Database()
con = test.open_connection()
x = pd.read_sql("SELECT * FROM access_control.funcionarios", con)
print(x.columns)
test.close_db()
"""



