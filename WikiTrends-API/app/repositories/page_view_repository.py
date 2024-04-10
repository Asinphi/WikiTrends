# page_view_repository.py
from sqlalchemy import text
from app.models.page_view import PageView

class PageViewRepository:
    def __init__(self, engine):
        self.engine = engine
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        table_name = 'PageView'
        table = f"""
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE {table_name} (
                    ArticleID INTEGER NOT NULL,
                    ViewDate DATE NOT NULL,
                    ViewCount INTEGER NOT NULL,
                    PRIMARY KEY (ArticleID, ViewDate),
                    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID)
                )';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -955 THEN
                        RAISE;
                    END IF;
            END;
        """

        try:
            with self.engine.connect() as connection:
                connection.execute(text(table))
                connection.commit()
                print(f"Table {table_name} created successfully.")
        except Exception as e:
            print(f"Error creating table {table_name}:\n", e)

    def get_by_article_id(self, article_id):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT ArticleID, ViewDate, ViewCount FROM PageView WHERE ArticleID = :article_id"), {'article_id': article_id})
            rows = result.fetchall()
            return [PageView(*row) for row in rows]

    def create(self, page_view):
        with self.engine.connect() as conn:
            try:
                result = conn.execute(text("SELECT ArticleID, ViewDate FROM PageView WHERE ArticleID = :article_id AND ViewDate = :view_date"), {'article_id': page_view.article_id, 'view_date': page_view.view_date})
                if result.fetchone() is None:
                    conn.execute(text("""
                        INSERT INTO PageView (ArticleID, ViewDate, ViewCount)
                        VALUES (:article_id, :view_date, :view_count)
                    """), {'article_id': page_view.article_id, 'view_date': page_view.view_date, 'view_count': page_view.view_count})
                    conn.commit()
                else:
                    print(f"PageView for ArticleID {page_view.article_id} and ViewDate {page_view.view_date} already exists.")
            except Exception as e:
                print(f"Error inserting page view into database:\n", e)
                conn.rollback()