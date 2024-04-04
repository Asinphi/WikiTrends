from flask import Flask
from config import Config
import cx_Oracle

app = Flask(__name__)
app.config.from_object(Config)

def test_db_connection():
    try:
        db_config = app.config['SQLALCHEMY_DATABASE_URI']
        with cx_Oracle.connect(db_config) as conn:
            print("Connected to Oracle database successfully!")
    except cx_Oracle.Error as e:
        print(f"Error connecting to Oracle database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_db_connection()
