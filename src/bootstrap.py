# bootstrap.py (in root)

from config.dotenv_loader import load_env
from config.logging_config import setup_logging
from config.logging_config import logger
from config.mlflow_tracking import configure_mlflow


def initialize_app():
    load_env()
    setup_logging()
    configure_mlflow()
    logger.info("Application bootstrap completed.")


if __name__ == "__main__":
    initialize_app()
