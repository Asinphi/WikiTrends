import logging
from flask import Flask
from config import Config
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object(Config)

def test_db_connection():
    try:
        db_config = app.config['SQLALCHEMY_DATABASE_URI']
        logging.debug(f"Database connection string: {db_config}")

        engine = create_engine(db_config)
        with engine.connect() as connection:
            logging.debug("Connected to Oracle database successfully!")
            logging.debug(f"Database version: {connection.dialect.server_version_info}")

    except Exception as e:
        logging.error(f"Error connecting to Oracle database: {e}")

if __name__ == "__main__":
    test_db_connection()