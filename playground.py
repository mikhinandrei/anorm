from anorm.core import BaseModel
from anorm.core import columns
from anorm.core.session import SessionStorage
import asyncio


class Album(BaseModel):
    title = columns.Varchar(max_length=256)
    year = columns.Integer()
    is_explicit = columns.Boolean()


async def async_main():
    await SessionStorage().connect("postgresql://mikhinandrei@localhost/anorm")
    print(await Album.repository.count())
    all_albums = await Album.repository.all()
    for album in all_albums:
        print(album.id, album.title, album.year, album.is_explicit)

    last_record = await Album.repository.last()

    print("Last record:", last_record.title, last_record.year, last_record.is_explicit)


asyncio.run(async_main())
