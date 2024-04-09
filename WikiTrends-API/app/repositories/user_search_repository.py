# user_search_repository.py
import oracledb
from app.models.user_search import UserSearch
from flask import current_app

class UserSearchRepository:
    def __init__(self):
        self.db_config = current_app.config['SQLALCHEMY_DATABASE_URI']
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS UserSearch (
                    SearchID INTEGER NOT NULL,
                    SearchDate DATE NOT NULL,
                    SearchTerm VARCHAR(255) NOT NULL,
                    PRIMARY KEY (SearchID)
                )
            """)
            cursor.execute("""
                CREATE SEQUENCE IF NOT EXISTS UserSearch_seq
                    START WITH 1
                    INCREMENT BY 1
                    NOMAXVALUE
            """)
            conn.commit()

    def get_by_search_term(self, search_term):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SearchID, SearchDate, SearchTerm FROM UserSearch WHERE SearchTerm = :search_term", search_term=search_term)
            row = cursor.fetchone()
            if row:
                search_id, search_date, search_term = row
                return UserSearch(search_id, search_date, search_term)
            return None

    def create(self, user_search):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO UserSearch (SearchID, SearchDate, SearchTerm)
                VALUES (UserSearch_seq.NEXTVAL, :search_date, :search_term)
            """, search_date=user_search.search_date, search_term=user_search.search_term)
            conn.commit()