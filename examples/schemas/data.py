from datetime import datetime, timedelta

import click
from schema import Parent
from sqlalchemy.orm import sessionmaker

from pgsync.base import pg_engine, subtransactions
from pgsync.helper import teardown
from pgsync.utils import config_loader, get_config


@click.command()
@click.option(
    "--config",
    "-c",
    help="Schema config",
    type=click.Path(exists=True),
)
def main(config):
    config: str = get_config(config)
    teardown(drop_db=False, config=config)
    document = next(config_loader(config))
    database: str = document.get("database", document["index"])
    with pg_engine(database) as engine:
        Session = sessionmaker(bind=engine, autoflush=True)
        session = Session()
        with subtransactions(session):
            session.add_all(
                [
                    Parent(id=1, name="Avocado", description="The fruit of domestic varieties have smooth, buttery, golden-green flesh when ripe. Depending on the cultivar, avocados have green, brown, purplish, or black skin, and may be pear-shaped, egg-shaped, or spherical. For commercial purposes the fruits are picked while unripe and ripened after harvesting. The nutrient density and extremely high fat content of avocado flesh are useful to a variety of cuisines and are often eaten to enrich vegetarian diets.",count_left="100",create_time=str(datetime.now()),update_time=str(datetime.now())),
                    Parent(id=2, name="Watermelon", description="is a flowering plant species of the Cucurbitaceae family and the name of its edible fruit. A scrambling and trailing vine-like plant, it is a highly cultivated fruit worldwide, with more than 1,000 varieties.",count_left="100",create_time=str(datetime.now()),update_time=str(datetime.now())),
                    Parent(id=3, name="lemon", description="is a species of small evergreen trees in the flowering plant family Rutaceae, native to Asia, primarily Northeast India (Assam), Northern Myanmar or China.",count_left="100",create_time=str(datetime.now()),update_time=str(datetime.now())),
                ]
            )


if __name__ == "__main__":
    main()
