# article_repository.py
from sqlalchemy import text
from app.models.article import Article

class ArticleRepository:
    def __init__(self, engine):
        self.engine = engine
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        table_name = 'Article'
        table = f"""
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE {table_name} (
                    ArticleID INTEGER NOT NULL,
                    Title VARCHAR2(255) NOT NULL,
                    PostDate DATE NOT NULL,
                    LastUpdated DATE NOT NULL,
                    PRIMARY KEY (ArticleID)
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

    def get_by_title(self, title):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT ArticleID, Title, PostDate, LastUpdated FROM Article WHERE Title = :title"), {'title': title})
            row = result.fetchone()
            if row:
                article_id, title, post_date, last_updated = row
                return Article(article_id, title, post_date, last_updated)
            return None

    def create(self, article):
        with self.engine.connect() as conn:
            try:
                result = conn.execute(text("SELECT ArticleID FROM Article WHERE ArticleID = :article_id"), {'article_id': article.article_id})
                if result.fetchone() is None:
                    conn.execute(text("""
                        INSERT INTO Article (ArticleID, Title, PostDate, LastUpdated)
                        VALUES (:article_id, :title, :post_date, :last_updated)
                    """), {'article_id': article.article_id, 'title': article.title, 'post_date': article.post_date, 'last_updated': article.last_updated})
                    conn.commit()
                else:
                    print(f"Article with ID {article.article_id} already exists.")
            except Exception as e:
                print(f"Error inserting article into database:\n", e)
                conn.rollback()