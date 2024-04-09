# page_view_repository.py
import oracledb
from app.models.page_view import PageView
from flask import current_app

class PageViewRepository:
    def __init__(self):
        self.db_config = current_app.config['SQLALCHEMY_DATABASE_URI']
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PageView (
                    ArticleID INTEGER NOT NULL,
                    ViewDate DATE NOT NULL,
                    ViewCount INTEGER NOT NULL,
                    PRIMARY KEY (ArticleID, ViewDate),
                    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID)
                )
            """)
            conn.commit()

    def get_by_article_id(self, article_id):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ArticleID, ViewDate, ViewCount FROM PageView WHERE ArticleID = :article_id", article_id=article_id)
            rows = cursor.fetchall()
            return [PageView(*row) for row in rows]

    def create(self, page_view):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PageView (ArticleID, ViewDate, ViewCount)
                VALUES (:article_id, :view_date, :view_count)
            """, article_id=page_view.article_id, view_date=page_view.view_date, view_count=page_view.view_count)
            conn.commit()