# category_repository.py
import oracledb
from app.models.category import Category
from flask import current_app

class CategoryRepository:
    def __init__(self):
        self.db_config = current_app.config['SQLALCHEMY_DATABASE_URI']
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Categories (
                    CategoryID INTEGER PRIMARY KEY,
                    CategoryName VARCHAR(255) NOT NULL,
                    ParentCategory INTEGER
                )
            """)
            cursor.execute("""
                CREATE SEQUENCE IF NOT EXISTS Categories_seq
                    START WITH 1
                    INCREMENT BY 1
                    NOMAXVALUE
            """)
            conn.commit()

    def get_by_name(self, category_name):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT CategoryID, CategoryName, ParentCategory FROM Categories WHERE CategoryName = :category_name", category_name=category_name)
            row = cursor.fetchone()
            if row:
                category_id, category_name, parent_category = row
                return Category(category_id, category_name, parent_category)
            return None

    def create(self, category):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Categories (CategoryID, CategoryName, ParentCategory)
                VALUES (Categories_seq.NEXTVAL, :category_name, :parent_category)
            """, category_name=category.category_name, parent_category=category.parent_category)
            conn.commit()

    def add_article_category(self, article_id, category_id):
        with oracledb.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS HasCategory (
                    ArticleID INTEGER NOT NULL,
                    CategoryID INTEGER NOT NULL,
                    PRIMARY KEY (ArticleID, CategoryID)
                )
            """)
            cursor.execute("""
                INSERT INTO HasCategory (ArticleID, CategoryID)
                VALUES (:article_id, :category_id)
            """, article_id=article_id, category_id=category_id)
            conn.commit()