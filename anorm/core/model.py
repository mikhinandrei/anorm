"""
Basic Model realization
"""
import asyncio
import asyncpg

from anorm.core import columns


class ModelMeta(type):
    def __new__(metacls, cls, bases, dct: dict):
        magic_attributes = {}
        _columns = {}
        for name, value in dct.items():
            if name.startswith('__'):
                magic_attributes[name] = value
            if isinstance(value, columns.BaseColumn):
                _columns[name] = value

        cls_attrs = {
            **magic_attributes,
            '_columns': _columns,
        }
        return super().__new__(metacls, cls, bases, cls_attrs)


class BaseModel(metaclass=ModelMeta):
    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            if name in self._columns:
                casted_value = self._columns[name].cast_python_value(value)
                setattr(self, name, casted_value)
