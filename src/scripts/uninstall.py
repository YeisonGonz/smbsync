import os

from loguru import logger
from src.Configuration import Configuration

cf = Configuration()

def uninstall():
    # To run this script, use the command: python3 -m src.scripts.uninstall

    db_path = cf.config.DATABASE_FILE_PATH

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            logger.success(f"{db_path} removed successfully!")
            db_dir = os.path.dirname(db_path)
            if not os.listdir(db_dir):
                os.rmdir(db_dir)
                logger.success(f"Directory {db_dir} removed successfully!")
            else:
                logger.warning(f"Directory {db_dir} is not empty, skipping removal.")
        except Exception as e:
            logger.error(f"Error removing file or directory: {e}")
    else:
        logger.warning(f"The file {db_path} does not exist.")

if __name__ == "__main__":
    uninstall()