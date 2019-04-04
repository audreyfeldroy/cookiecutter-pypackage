from apphelpers.peewee.db import create_pgdb_pool, create_base_model, created

import settings

db = create_pgdb_pool(database=settings.DB_NAME)
BaseModel = create_base_model(db)


class CommonModel(BaseModel):
    created = created()


# Model definitions goes here

# class AModel(CommonModel):
#    lang = TextField(default="en")

# Setup helpers

the_models = BaseModel.__subclasses__() + CommonModel.__subclasses__()


def setup_db():
    db.create_tables(the_models, fail_silently=True)


def destroy_db():
    for o in the_models[::-1]:
        if o.table_exists():
            o.drop_table()
            print("DROP: " + o._meta.name)
