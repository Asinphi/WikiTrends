import cx_Oracle

class CategoryRepository:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def get_by_name(self, category_name):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Categories WHERE CategoryName = :category_name", category_name=category_name)
            row = cursor.fetchone()
            if row:
                return Category(*row)
            return None
    
    def create(self, category):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Categories (CategoryID, CategoryName, ParentCategory)
                VALUES (:category_id, :category_name, :parent_category)
            """, category.__dict__)
            conn.commit()
    
    def add_article_category(self, article_id, category_id):
        with cx_Oracle.connect(self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO HasCategory (ArticleID, CategoryID)
                VALUES (:article_id, :category_id)
            """, article_id=article_id, category_id=category_id)
            conn.commit()