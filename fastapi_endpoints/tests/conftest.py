import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from core import config

TEST_SCHEMA = "pytest_isolated"
with config.engine.begin() as connection:
    connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{TEST_SCHEMA}"'))
config.engine.dispose()

test_engine = create_engine(
    config.DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"options": f"-csearch_path={TEST_SCHEMA}"},
)
config.engine = test_engine
config.SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

from db.database import Base

Base.metadata.create_all(test_engine)