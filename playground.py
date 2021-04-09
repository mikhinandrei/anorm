from anorm.core import BaseModel
from anorm.core import columns


class Album(BaseModel):
    title = columns.Varchar()
    year = columns.Integer()


a = Album(title="Master of puppets", year=1986)
print(a.__dict__)
