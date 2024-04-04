import cx_Oracle

class ArticleRepository:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def get_by_title(self, title):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Article WHERE Title = :title", title=title)
            row = cursor.fetchone()
            if row:
                return Article(*row)
            return None
    
    def create(self, article):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Article (ArticleID, Title, PostDate, LastUpdated)
                VALUES (:article_id, :title, :post_date, :last_updated)
            """, article.__dict__)
            conn.commit()