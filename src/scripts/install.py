import sqlite3
import json
import uuid
import os
from loguru import logger
from src.Configuration import Configuration

cf = Configuration()

def make_installation():
    # To run this script, use the command: python3 -m src.scripts.install

    db_path = cf.config.DATABASE_FILE_PATH

    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)

    if not os.path.exists(cf.config.KEY_PATH):
        make_uuid_encrypt()

    if os.path.exists(cf.config.DATABASE_FILE_PATH):
        logger.info(f"File {cf.config.DATABASE_FILE_PATH} exists!")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS samba_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            host_connection TEXT NOT NULL
        )
        """)

        conn.commit()
        conn.close()
        logger.success(f"Lite database created successfully")
    except sqlite3.OperationalError as e:
        logger.error(f"Error al conectar a la base de datos: {e}")


def make_uuid_encrypt():
    """Genera un UUID y lo guarda en un archivo JSON para encriptación."""
    encryption_uuid = str(uuid.uuid4())

    config_data = {"encryption_key": encryption_uuid}

    with open(cf.config.KEY_PATH, "w") as f:
        json.dump(config_data, f, indent=4)

    logger.success(f"Encryption Key created successfully")


if __name__ == '__main__':
    make_installation()
