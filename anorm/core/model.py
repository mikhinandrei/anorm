"""
Basic Model realization
"""
import asyncio
import asyncpg

from anorm.core import columns
from typing import Dict, List


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
