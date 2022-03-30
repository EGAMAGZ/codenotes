import os
from typing import AnyStr, Final

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR: Final[AnyStr] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_NAME: Final[str] = "codenotes_sql.db"
DATABASE_PATH: Final[str] = os.path.join(BASE_DIR, DATABASE_NAME)

engine = create_engine(f"sqlite:///{DATABASE_PATH}", future=True)
Session = sessionmaker(engine)
session = Session()

Base = declarative_base()
