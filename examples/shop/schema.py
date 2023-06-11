from datetime import datetime

import click
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint
import sqlmodel

from pgsync.base import create_database, pg_engine
from pgsync.helper import teardown
from pgsync.utils import config_loader, get_config

Base = declarative_base()


class Shop(Base):
    __tablename__ = "shop"
    __table_args__ = (UniqueConstraint("name","description","count_left","create_time","update_time"),)
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False)
    description = sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False)
    count_left = sa.Column('count_left', sa.Integer(), nullable=False)
    create_time = sa.Column('create_time', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False)
    update_time = sa.Column('update_time', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False)



def setup(config: str) -> None:
    for document in config_loader(config):
        database: str = document.get("database", document["index"])
        create_database(database)
        with pg_engine(database) as engine:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)


@click.command()
@click.option(
    "--config",
    "-c",
    help="Schema config",
    type=click.Path(exists=True),
)
def main(config):
    config: str = get_config(config)
    teardown(config=config)
    setup(config)


if __name__ == "__main__":
    main()
