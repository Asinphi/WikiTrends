from sqlalchemy import text
from app.models.user_search import UserSearch
from app.models.article import Article
from app.models.page_view import PageView

class UserSearchRepository:
    def __init__(self, engine):
        self.engine = engine
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        table_name = 'UserSearch'
        table = f"""
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE {table_name} (
                    SearchID INTEGER NOT NULL,
                    SearchDate DATE NOT NULL,
                    SearchTerm VARCHAR2(255) NOT NULL,
                    PRIMARY KEY (SearchID)
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
                EXECUTE IMMEDIATE 'CREATE SEQUENCE UserSearch_seq
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


    def create(self, user_search):
        with self.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO UserSearch (SearchID, SearchDate, SearchTerm)
                VALUES (UserSearch_seq.NEXTVAL, :search_date, :search_term)
            """), {'search_date': user_search.search_date, 'search_term': user_search.search_term})
            conn.commit()
            print(f"Inserted user search for term '{user_search.search_term}' on {user_search.search_date}.")

    def count(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM UserSearch"))
            return result.scalar()
        
    def get_search_results(self, search_term):
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT a.ArticleID, a.Title, a.PostDate, a.LastUpdated, p.ViewDate, p.ViewCount, 
                    SUM(p.ViewCount) OVER (PARTITION BY a.ArticleID) AS TotalViews
                FROM Article a
                JOIN PageView p ON a.ArticleID = p.ArticleID
                WHERE a.Title LIKE :search_term
                ORDER BY TotalViews DESC
            """), {'search_term': f'%{search_term}%'})
            rows = result.fetchall()

            articles = {}
            for row in rows:
                article_id, title, post_date, last_updated, view_date, view_count, total_views = row
                if article_id not in articles:
                    articles[article_id] = {
                        'article': Article(title=title, article_id=article_id, post_date=post_date, last_updated=last_updated, total_views=total_views),
                        'page_views': []
                    }
                articles[article_id]['page_views'].append(PageView(article_id=article_id, view_date=view_date, view_count=view_count))

            return [{'article': data['article'], 'page_views': data['page_views']} for data in articles.values()]
    
    def get_by_search_term(self, search_term):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM SearchResults WHERE Title = :search_term"), {'search_term': search_term})
            row = result.fetchone()
            if row:
                search_term, total_views = row
                return UserSearch(search_term=search_term, total_views=total_views)
            return None