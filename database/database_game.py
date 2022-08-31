# Imports
import os
# Hint Types
from dataclasses import dataclass, field
import sqlalchemy  # Used to the hint types of the attributes
# DataBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


@dataclass
class DataBaseGame:

    ROOT_DB: str = r'sqlite:///C:\Users\albin\PycharmProjects\dice_&_die\database\game.db'

    engine: sqlalchemy.engine.base.Engine = None
    base: sqlalchemy.orm.decl_api.DeclarativeMeta = field(default_factory=declarative_base)
    session: sqlalchemy.orm.session.Session = None

    def __post_init__(self):
        self.create_engine()
        self.create_session()

    def create_engine(self):
        self.engine = create_engine(os.environ.get('DATABASE_URL_DICE') or self.ROOT_DB)

    def create_session(self):
        Session = sessionmaker(self.engine)
        self.session = Session()


