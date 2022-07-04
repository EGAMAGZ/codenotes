from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from codenotes.utils import get_base_dir

BASE_DIR = get_base_dir()

DATABASE_NAME = "codenotes_sql.db"
DATABASE_PATH = BASE_DIR / DATABASE_NAME

engine = create_engine(f"sqlite:///{DATABASE_PATH}")
Session = sessionmaker()
Session.configure(bind=engine)

Base = declarative_base()
