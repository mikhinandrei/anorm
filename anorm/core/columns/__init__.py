from abc import ABC, abstractmethod


class BaseColumn(ABC):
    def __init__(self,
        primary_key: bool=False,
        db_index: bool=False,
    ):
        self.primary_key = primary_key
        self.db_index = db_index
        if primary_key:
            self.db_index = True
    
    @abstractmethod
    def cast_python_value(self, value):
        """
        Try to cast value to column type
        """
        pass

    @abstractmethod
    def sql_type(self):
        """
        SQL type for CREATE TABLE
        """
        pass
    
    @abstractmethod
    def to_db(self):
        """
        Function which prepares field as sql
        """
        pass

    @abstractmethod
    def to_python(self, value):
        """
        Represent db value as python value
        """
        pass


class Varchar(BaseColumn):
    def sql_type(self):
        "VARCHAR"
    
    def cast_python_value(self, value):
        return str(value)

    def to_db(self):
        pass

    def to_python(self, value):
        return str(value)