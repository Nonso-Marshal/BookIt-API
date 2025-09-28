from logging.config import fileConfig
from logging import basicConfig, INFO
from sqlalchemy import engine_from_config, pool
from database import engine
from models import User, Service, Booking, Review
from base import Base
import os
import sys

from alembic import context

print("sys.path:", sys.path)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("Adding project root to sys.path:", project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

base_path = os.path.join(project_root, 'base.py')
print("Checking for base.py at:", base_path, "Exists:", os.path.exists(base_path))

from base import Base
from database import engine
import models 

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()