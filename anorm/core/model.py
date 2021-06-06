"""
Basic Model realization
"""
import asyncio
import asyncpg
from anorm.core.session import SessionStorage
from anorm.core.conditions import QueryConditions

from anorm.core import columns
from typing import Dict, List


class LazyQuery:
    def __init__(self, output_model, conditions: dict = {}):
        self._output_model = output_model
        self.conditions = conditions

    def _convert_to_output_model(self, record: asyncpg.Record):
        data_dict = {}
        for column_name, column in self._output_model._columns.items():
            data_dict[column_name] = column.cast_python_value(record[column_name])

        return self._output_model(**data_dict)

    async def all(self):
        """
        Get all entries matching query
        :usage:
        MyModel.repository.filter(**conditions).all()

        :return: List[MyModel]
        """
        async with SessionStorage.get_pool().acquire() as cursor:
            records: List[asyncpg.Record] = await cursor.fetch(
                """
                    SELECT * FROM {table_name}
                    {where_conditions}
                """.format(
                    table_name=self._output_model.__tablename__,
                    where_conditions=QueryConditions(self.conditions).to_sql_where(),
                )
            )

            result = [self._convert_to_output_model(record) for record in records]

            return result

    async def count(self) -> int:
        async with SessionStorage.get_pool().acquire() as cursor:
            result = await cursor.fetch(
                """
                    SELECT COUNT(*) FROM {table_name}
                    {where_conditions}
                """.format(
                    table_name=self._output_model.__tablename__,
                    where_conditions=QueryConditions(self.conditions).to_sql_where(),
                )
            )
            return int(result[0]["count"])

    async def last(self):
        async with SessionStorage.get_pool().acquire() as cursor:
            result = await cursor.fetch(
                """
                    SELECT * FROM {table_name}
                        ORDER BY id DESC
                """.format(
                    table_name=self._output_model.__tablename__
                )
            )
            return self._convert_to_output_model(result[0])

    async def first(self):
        async with SessionStorage.get_pool().acquire() as cursor:
            result = await cursor.fetch(
                """
                    SELECT * FROM {table_name}
                        ORDER BY id ASC
                """.format(
                    table_name=self._output_model.__tablename__
                )
            )
            return self._convert_to_output_model(result[0])

    async def get_or_none(self):
        async with SessionStorage.get_pool().acquire() as cursor:
            result = await cursor.fetch(
                """
                    SELECT * FROM {table_name}
                        ORDER BY id ASC
                """.format(
                    table_name=self._output_model.__tablename__
                )
            )

            if len(result) == 0:
                return None

            return self._convert_to_output_model(result[0])

    async def update(self):
        pass

    async def create(self):
        pass

    async def delete(self):
        pass


class Repository:
    """
    Class used as lazy queries factory
    """

    def __init__(self, owner_model):
        self._owner_model = owner_model

    def filter(self, **conditions) -> LazyQuery:
        conditions_dict = {}
        for column_name, condition_value in conditions.items():
            if column_name not in self._owner_model._columns:
                raise Exception(f"Unknown column {column_name}")
            conditions_dict[column_name] = self._owner_model._columns[
                column_name
            ].cast_python_value(condition_value)
        return LazyQuery(output_model=self._owner_model, conditions=conditions_dict)

    # Proxy methods to LazyQuery
    async def all(self):
        return await LazyQuery(output_model=self._owner_model).all()

    async def count(self):
        return await LazyQuery(output_model=self._owner_model).count()

    async def last(self):
        return await LazyQuery(output_model=self._owner_model).last()

    async def get_or_none(self):
        return await LazyQuery(output_model=self._owner_model).get_or_none()

    async def update(self):
        return await LazyQuery(output_model=self._owner_model).update()


class ModelMeta(type):
    def __new__(metacls, cls, bases, dct: dict):
        tablename = dct.pop("__tablename__", cls.lower() + "s")
        _id_column = None

        magic_attributes = {}
        _columns = {}
        other_attributes = {}

        for name, value in dct.items():
            if name.startswith("__"):
                magic_attributes[name] = value
            elif isinstance(value, columns.BaseColumn):
                _columns[name] = value
                if isinstance(value, columns.Serial):
                    if _id_column:
                        raise Exception("Only one serial column allowed!")

                    _id_column = name
            else:
                other_attributes[name] = value

        if not _id_column:
            _id_column = "id"
            _columns[_id_column] = columns.Serial()

        repository_class = dct.get("repository", Repository)

        cls_attrs = {
            **magic_attributes,
            **other_attributes,
            "_columns": _columns,
            "repository": repository_class(cls.__class__),
            "__tablename__": tablename,
            "_id_column": _id_column,
        }

        instant_class = super().__new__(metacls, cls, bases, cls_attrs)
        setattr(instant_class, "repository", repository_class(instant_class))

        return instant_class


class BaseModel(metaclass=ModelMeta):
    _columns: Dict[str, columns.BaseColumn]

    def __init__(self, *args, **kwargs):
        self.repository: Repository = None
        for column_name, model_column in self._columns.items():
            input_value = kwargs.get(column_name, model_column.default_value)
            casted_value = model_column.cast_python_value(input_value)
            setattr(self, column_name, casted_value)

    def to_json(self):
        result = {}
        for column_name in self._columns:
            result[column_name] = getattr(self, column_name)

        return result

    def update(self, **data):
        print("lol")

    def delete(self):
        pass
