import pytest
from anorm.core import BaseModel
from anorm.core import columns


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            {
                'title': 'Master of Puppets',
                'year': 1986,
            },
            {
                'title': 'Master of Puppets',
                'year': 1986,
            },
        ),
        (
            {
                'title': 'Master of Puppets',
                'year': '1986',
            },
            {
                'title': 'Master of Puppets',
                'year': 1986,
            },
        ),
    ]
)
def test_create_simple_types_success(input, expected):
    class Album(BaseModel):
        title = columns.Varchar(32)
        year = columns.Integer()

    album = Album(**input)
    assert album.__dict__ == expected
