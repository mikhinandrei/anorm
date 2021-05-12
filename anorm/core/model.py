"""
Basic Model realization
"""
import asyncio
import asyncpg
from anorm.core.session import SessionStorage

from anorm.core import columns
from typing import Dict, List


class LazyQuery:
    def __init__(self, output_model, **conditions):
        self._output_model = output_model

    async def all(self):
        """
        Get all entries matching query
        :usage:
        MyModel.repository.filter(**conditions).all()

        :return: List[MyModel]
        """
        async with SessionStorage.get_pool().acquire() as cursor:
            await cursor.execute(
                """
                SELECT * FROM {}
            """
            )
            rows: List[asyncpg.Record] = cursor.fetch()

    async def count(self):
        pass

    async def last(self):
        pass

    async def first(self):
        pass

    async def get_or_none(self):
        pass

    async def update(self):
        pass


class Repository:
    """
    Class used as lazy queries factory
    """

    def __init__(self, owner_model):
        self._owner_model = owner_model

    def filter(self, **kwargs) -> LazyQuery:
        return LazyQuery(output_model=self._owner_model)


class ModelMeta(type):
    def __new__(metacls, cls, bases, dct: dict):
        magic_attributes = {}
        _columns = {}
        for name, value in dct.items():
            if name.startswith("__"):
                magic_attributes[name] = value
            if isinstance(value, columns.BaseColumn):
                _columns[name] = value

        cls_attrs = {
            **magic_attributes,
            "_columns": _columns,
        }
        return super().__new__(metacls, cls, bases, cls_attrs)


class BaseModel(metaclass=ModelMeta):
    _columns: Dict[str, columns.BaseColumn]

    def __init__(self, *args, **kwargs):
        for column_name, model_column in self._columns.items():
            input_value = kwargs.get(column_name, model_column.default_value)
            casted_value = model_column.cast_python_value(input_value)
            setattr(self, column_name, casted_value)

        repository_class = kwargs.get("repository", Repository)
        self.repository = repository_class(self.__class__)
