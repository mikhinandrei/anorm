from anorm.core import BaseModel
from anorm.core import columns


class Album(BaseModel):
    title = columns.Varchar()


a = Album(title="Master of puppets")
