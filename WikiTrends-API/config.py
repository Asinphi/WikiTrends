from sqlalchemy import create_engine

class Config:
    USER = 'terry.nelson'
    PASSWORD = '6G8IWcIQQsswp0Rw7hN1X6qO'
    HOST = 'oracle.cise.ufl.edu'
    PORT = '1521'
    SID = 'orcl'

    SQLALCHEMY_DATABASE_URI = f'oracle+cx_oracle://{USER}:{PASSWORD}@{HOST}:{PORT}/?service_name={SID}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db_config = create_engine(Config.SQLALCHEMY_DATABASE_URI)