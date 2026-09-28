from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
engine = create_engine(
    "sqlite:///dev_db.db",
    connect_args={"check_same_thread": False}
)
# LATER переход на Postgres

Session = sessionmaker(autoflush=False, bind=engine, autocommit=False)

Base.metadata.create_all(engine)