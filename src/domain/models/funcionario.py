from abc import ABC, abstractmethod

class Funcionario(ABC):

    @abstractmethod
    def __init__(self, name: str, cpf: int, tel:int, password:str, cargo: str):
        self.__name = None
        self.__cpf = None
        self.__tel = None
        self.__password = None
        self.__cargo = None
        if isinstance(name, str):
            self.__name = name
        if isinstance(cpf, int):
            self.__cpf = cpf
        if isinstance(tel, int):
            self.__tel = tel
        if isinstance(password, str):
            self.__password = password
        if isinstance(cargo, str):
            self.__cargo = cargo

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name: str):
        if isinstance(name, str):
            self.__name = name

    @property
    def cpf(self):
        return self.__cpf
    @cpf.setter
    def cpf(self, cpf: int):
        if isinstance(cpf, int):
            self.__cpf = cpf

    @property
    def cargo(self):
        return self.__cargo
    @cargo.setter
    def tel(self, cargo: str):
        if isinstance(cargo, str):
            self.__cargo = cargo

    @property
    def tel(self):
        return self.__tel
    @tel.setter
    def tel(self, tel: int):
        if isinstance(tel, int):
            self.__tel = tel

    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, password: str):
        if isinstance(password, str):
            self.__password = password