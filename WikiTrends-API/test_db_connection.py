import logging
from flask import Flask
from config import Config
import oracledb

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object(Config)

def test_db_connection():
    try:
        db_config = app.config['SQLALCHEMY_DATABASE_URI']
        logging.debug(f"Database connection string: {db_config}")

        with oracledb.connect(db_config) as conn:
            logging.debug("Connected to Oracle database successfully!")
            logging.debug(f"Database version: {conn.version}")

    except oracledb.Error as e:
        error_obj, = e.args
        logging.error(f"Error connecting to Oracle database: {e}")
        logging.error(f"Error code: {error_obj.code}")
        logging.error(f"Error message: {error_obj.message}")
        logging.error(f"Error context: {error_obj.context}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_db_connection()