import logging
from flask import Flask
from config import Config
import cx_Oracle

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object(Config)

def test_db_connection():
    try:
        db_config = app.config['SQLALCHEMY_DATABASE_URI']
        logging.debug(f"Database connection string: {db_config}")

        # Enable Oracle Client tracing
        logging.debug("Initializing Oracle Client")
        cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_13")  # Path to Oracle Instant Client directory
        logging.debug("Oracle Client initialized")

        with cx_Oracle.connect(db_config) as conn:
            logging.debug("Connected to Oracle database successfully!")
            logging.debug(f"Database version: {conn.version}")
            logging.debug(f"Client version: {cx_Oracle.clientversion()}")

    except cx_Oracle.Error as e:
        error_obj, = e.args
        logging.error(f"Error connecting to Oracle database: {e}")
        logging.error(f"Error code: {error_obj.code}")
        logging.error(f"Error message: {error_obj.message}")
        logging.error(f"Error context: {error_obj.context}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_db_connection()
