# asql
## What do I want
* Automatic session control (not like in sqlalchemy where required get and close sessions)
* Code-first migrations
* Model definitions (Think about type annotations):
```python
class Album(BaseModel):
    album_id = Columns.Auto() # autoincrement primary key
    title = Columns.String(max_length=32)
    description = Columns.Text()
    publication_date = Columns.Date()
    is_explicit = Columns.Boolean()
```
generates migration (migrations allowed to be sync)
```postgresql
CREATE TABLE albums (
    album_id SERIAL,
    title VARCHAR(32),
    description TEXT,
    publication_date DATE,
    is_explicit BOOLEAN
);
```
* Queries:
   Repository attribute (repositories auto-generated)
```python
# create
master_of_puppets_album = await Album.repository.create(
    title='Master of puppets',
    description='Obey your master'
    publication_date=datetime.now(),
    is_explicit=True,
)

# find list
albums = await Album.repository.find(
    title={'like': 'Master'}   # Not beautiful
)

# get
some_album = await Album.repository.get(ALBUM_ID)

# safe get
safe_album = await Album.repository.get_or_none(ALBUM_ID)

#update
safe_album_updated = await safe_album.update(
    publication_date=datetime(1986, 3, 3)
)
```

## ToDo: think about relations
