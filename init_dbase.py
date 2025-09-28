import logging
from alembic.config import Config
from alembic import command
from database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        if  engine is None:
            raise Exception("Database engine not initialized. check DATABASE_URL")
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
        command.upgrade(alembic_cfg, "head")
        logger.info("Database tables created successfully via Alembic!")
    except Exception as error:
        logger.error(f"Failed to create database tables: {str(error)}")
        raise

if __name__ == "__main__":
    init_db()