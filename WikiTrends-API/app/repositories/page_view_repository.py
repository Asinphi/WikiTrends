import cx_Oracle

class PageViewRepository:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def get_by_article_id(self, article_id):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PageView WHERE ArticleID = :article_id", article_id=article_id)
            rows = cursor.fetchall()
            return [PageView(*row) for row in rows]
    
    def create(self, page_view):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PageView (ArticleID, ViewDate, ViewCount)
                VALUES (:article_id, :view_date, :view_count)
            """, page_view.__dict__)
            conn.commit()

