from abc import ABC, abstractmethod
from typing import Any


class BaseColumn(ABC):
    def __init__(self,
        primary_key: bool=False,
        db_index: bool=False,
        default_value: Any = None,
        nullable: bool = True,
    ):
        if not (nullable and default_value is None):
            raise Exception
        if primary_key:
            db_index = True

        self.primary_key = primary_key
        self.db_index = db_index
        self.nullable = nullable
        self.default_value = default_value
    
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
    def sql_type(self) -> str:
        return "VARCHAR"
    
    def cast_python_value(self, value):
        return str(value)

    def to_db(self):
        pass

    def to_python(self, value):
        return str(value)


class Integer(BaseColumn):
    def sql_type(self) -> str:
        return "INTEGER"
    
    def cast_python_value(self, value) -> int:
        return int(value)

    def to_db(self):
        pass

    def to_python(self, value) -> int:
        return int(value)


class Boolean(BaseColumn):
    def sql_type(self) -> str:
        return "BOOLEAN"
    
    def cast_python_value(self, value) -> bool:
        return bool(value)

    def to_db(self):
        pass

    def to_python(self, value) -> bool:
        return bool(value)


class Serial(BaseColumn):
    def __init__(self, *args, **kwargs):
        kwargs['primary_key'] = True
        kwargs['db_index'] = True

        super().__init__(*args, **kwargs)

    def sql_type(self) -> str:
        return "SERIAL"
    
    def cast_python_value(self, value) -> int:
        return int(value)

    def to_db(self):
        pass

    def to_python(self, value) -> int:
        return int(value)
