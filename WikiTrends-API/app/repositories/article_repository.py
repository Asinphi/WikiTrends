# article_repository.py
import cx_Oracle
from app.models.article import Article
from flask import current_app

class ArticleRepository:
    def __init__(self):
        self.db_config = current_app.config['SQLALCHEMY_DATABASE_URI']
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Article (
                    ArticleID INTEGER NOT NULL,
                    Title VARCHAR(255) NOT NULL,
                    PostDate DATE NOT NULL,
                    LastUpdated DATE NOT NULL,
                    PRIMARY KEY (ArticleID)
                )
            """)
            conn.commit()

    def get_by_title(self, title):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ArticleID, Title, PostDate, LastUpdated FROM Article WHERE Title = :title", title=title)
            row = cursor.fetchone()
            if row:
                article_id, title, post_date, last_updated = row
                return Article(article_id, title, post_date, last_updated)
            return None

    def create(self, article):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Article (ArticleID, Title, PostDate, LastUpdated)
                VALUES (:article_id, :title, :post_date, :last_updated)
            """, article.__dict__)
            conn.commit()