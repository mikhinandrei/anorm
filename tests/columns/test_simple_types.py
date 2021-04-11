import pytest
from anorm.core import columns
from anorm.core.expceptions import DataTypeException


def test_integer_column():
    col = columns.Integer()

    assert col.sql_type() == "INTEGER"

    assert col.cast_python_value(123) == 123
    assert col.cast_python_value('123') == 123

    assert col.cast_python_value(True) == 1  # IDK if it is a bug

    with pytest.raises(DataTypeException):
        col.cast_python_value('lorem')
    


def test_varchar_column():
    with pytest.raises(TypeError): #  Maybe provide custom exception?
        col = columns.Varchar()
    
    col = columns.Varchar(max_length=6)

    assert col.sql_type() == "VARCHAR"

    assert col.cast_python_value(123) == '123'
    assert col.cast_python_value('123') == '123'

    assert col.cast_python_value(True) == 'True'


def test_boolean_column():
    col = columns.Boolean()

    assert col.sql_type() == "BOOLEAN"

    assert col.cast_python_value(True) == True
    assert col.cast_python_value(False) == False
    assert col.cast_python_value(0) == False
    assert col.cast_python_value(12321423) == True

    assert col.cast_python_value('tRUE') == True
    assert col.cast_python_value('FalSe') == False

    with pytest.raises(DataTypeException):
        col.cast_python_value('')
    
    with pytest.raises(DataTypeException):
        col.cast_python_value('Some string')


def test_serial_column():
    col = columns.Serial()

    assert col.sql_type() == "SERIAL"
    assert col.db_index == True
    assert col.primary_key == True

    assert col.cast_python_value(123) == 123
    assert col.cast_python_value('123') == 123

    assert col.cast_python_value(True) == 1  # IDK if it is a bug

    with pytest.raises(DataTypeException):
        col.cast_python_value('lorem')
