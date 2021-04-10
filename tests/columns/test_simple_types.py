import pytest
from anorm.core import columns


def test_integer_column():
    col = columns.Integer()

    assert col.sql_type() == "INTEGER"


def test_varchar_column():
    col = columns.Varchar()

    assert col.sql_type() == "VARCHAR"


def test_boolean_column():
    col = columns.Boolean()

    assert col.sql_type() == "BOOLEAN"


def test_serial_column():
    col = columns.Serial()

    assert col.sql_type() == "SERIAL"
    assert col.db_index == True
    assert col.primary_key == True
