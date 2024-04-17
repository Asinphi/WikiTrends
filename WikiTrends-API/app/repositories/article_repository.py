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
        sequence = f"""
            BEGIN
                EXECUTE IMMEDIATE 'CREATE SEQUENCE ArticleID_seq
                    START WITH 1
                    INCREMENT BY 1
                    NOMAXVALUE';
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
                connection.execute(text(sequence))
                connection.commit()
                print(f"Table {table_name} and sequence created successfully.")
        except Exception as e:
            print(f"Error creating table {table_name} or sequence:\n", e)


    def get_by_title(self, title):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT ArticleID, Title, PostDate, LastUpdated FROM Article WHERE Title = :title"), {'title': title})
            row = result.fetchone()
            if row:
                article_id, title, post_date, last_updated = row
                return Article(article_id, title, post_date, last_updated)
            return None
    
    def get_by_date(self, date):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT ArticleID, Title, PostDate, LastUpdated FROM Article WHERE PostDate = :date"), {'date': date})
            row = result.fetchone()
            if row:
                article_id, title, post_date, last_updated = row
                return Article(article_id, title, post_date, last_updated)
            return None

        
    def create(self, article):
        with self.engine.connect() as conn:
            try:
                # Check if an article with the same title already exists
                result = conn.execute(text("SELECT ArticleID FROM Article WHERE Title = :title"), {'title': article.title})
                if result.fetchone() is not None:
                    print(f"Skipping insertion of article '{article.title}' as it already exists.")
                    return None

                result = conn.execute(text("SELECT ArticleID_seq.NEXTVAL FROM DUAL"))
                article_id = result.fetchone()[0]
                article.article_id = article_id
                conn.execute(text("""
                    INSERT INTO Article (ArticleID, Title, PostDate, LastUpdated)
                    VALUES (:article_id, :title, :post_date, :last_updated)
                """), {'article_id': article.article_id, 'title': article.title, 'post_date': article.post_date, 'last_updated': article.last_updated})
                conn.commit()
                print(f"Inserted article '{article.title}' with ID {article_id}.")
                return article_id
            except Exception as e:
                print(f"Error inserting article '{article.title}' into database:\n", e)
                conn.rollback()
                raise
            
    def count(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM Article"))
            return result.scalar()
        
    def create_long_lost_articles_view(self):
        with self.engine.connect() as conn:
            conn.execute(text("""
                CREATE OR REPLACE VIEW LongLostArticles AS
                SELECT Title, MIN(ViewDate) AS LastSeen, SUM(ViewCount) AS TotalViews
                FROM Article JOIN PageView ON Article.ArticleID = PageView.ArticleID
                GROUP BY Title
                HAVING MIN(ViewDate) < (CURRENT_DATE) AND SUM(ViewCount) <= 100
                ORDER BY dbms_random.value
                FETCH FIRST 1 ROWS ONLY
            """))
            conn.commit()
            print("View LongLostArticles created successfully.")

    def create_top_three_view(self):
        with self.engine.connect() as conn:
            conn.execute(text("""
                CREATE OR REPLACE VIEW TopThree AS
                SELECT Title, SUM(ViewCount) AS TotalViews
                FROM Article, PageView
                WHERE ViewDate = '30-JULY-23' AND Article.ArticleID = PageView.ArticleID
                GROUP BY Title
                ORDER BY TotalViews DESC
                FETCH FIRST 3 ROWS ONLY
            """))
            conn.commit()
            print("View TopThree created successfully.")

    def get_long_lost_article(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM LongLostArticles"))
            row = result.fetchone()
            if row:
                title, last_seen, total_views = row
                return Article(title=title, last_seen=last_seen, total_views=total_views)
            return None

    def get_top_three_articles(self, date):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM TopThree WHERE ViewDate = :date"), {'date': date})
            rows = result.fetchall()
            return [Article(title=row[0], total_views=row[1]) for row in rows]