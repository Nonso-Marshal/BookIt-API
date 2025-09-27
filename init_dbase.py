import logging
from alembic.config import Config
from alembic import command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database tables created successfully via Alembic!")
    except Exception as error:
        logger.error(f"Failed to create database tables: {str(error)}")
        raise

if __name__ == "__main__":
    init_db()