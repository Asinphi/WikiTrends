from sqlalchemy import text
from app.models.category import Category

class CategoryRepository:
    def __init__(self, engine):
        self.engine = engine
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        table_name = 'Category'
        table = f"""
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE {table_name} (
                    CategoryID INTEGER PRIMARY KEY,
                    CategoryName VARCHAR2(255) NOT NULL,
                    CategoryLink VARCHAR2(255),
                    ParentCategory VARCHAR2(255)
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
                EXECUTE IMMEDIATE 'CREATE SEQUENCE Category_seq
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

    def get_by_name(self, category_name):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT CategoryID, CategoryName, CategoryLink, ParentCategory FROM Category WHERE CategoryName = :category_name"), {'category_name': category_name})
            row = result.fetchone()
            if row:
                category_id, category_name, category_link, parent_category = row
                return Category(category_id, category_name, category_link, parent_category)
            return None

    def create(self, category):
        with self.engine.connect() as conn:
            try:
                result = conn.execute(text("SELECT CategoryID FROM Category WHERE CategoryName = :category_name"), {'category_name': category.category_name})
                if result.fetchone() is None:
                    if category.category_link is None:
                        conn.execute(text("""
                            INSERT INTO Category (CategoryID, CategoryName, ParentCategory)
                            VALUES (Category_seq.NEXTVAL, :category_name, :parent_category)
                        """), {'category_name': category.category_name, 'parent_category': category.parent_category})
                    else:
                        conn.execute(text("""
                            INSERT INTO Category (CategoryID, CategoryName, CategoryLink, ParentCategory)
                            VALUES (Category_seq.NEXTVAL, :category_name, :category_link, :parent_category)
                        """), {'category_name': category.category_name, 'category_link': category.category_link, 'parent_category': category.parent_category})
                    conn.commit()
                else:
                    print(f"Category with name {category.category_name} already exists.")
            except Exception as e:
                print(f"Error inserting category into database:\n", e)
                conn.rollback()

    def add_article_category(self, article_id, category_id):
        table_name = 'HasCategory'
        table = f"""
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE {table_name} (
                    ArticleID INTEGER NOT NULL,
                    CategoryID INTEGER NOT NULL,
                    PRIMARY KEY (ArticleID, CategoryID),
                    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID),
                    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
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
                
                if article_id is not None and category_id is not None:
                    # Check if ArticleID exists in the Article table
                    article_result = connection.execute(text("SELECT ArticleID FROM Article WHERE ArticleID = :article_id"), {'article_id': article_id})
                    if article_result.fetchone() is None:
                        print(f"Skipping insertion into HasCategory as ArticleID {article_id} does not exist in the Article table.")
                        return

                    # Check if CategoryID exists in the Category table
                    category_result = connection.execute(text("SELECT CategoryID FROM Category WHERE CategoryID = :category_id"), {'category_id': category_id})
                    if category_result.fetchone() is None:
                        print(f"Skipping insertion into HasCategory as CategoryID {category_id} does not exist in the Category table.")
                        return

                    result = connection.execute(text("SELECT ArticleID, CategoryID FROM HasCategory WHERE ArticleID = :article_id AND CategoryID = :category_id"), {'article_id': article_id, 'category_id': category_id})
                    if result.fetchone() is None:
                        connection.execute(text("""
                            INSERT INTO HasCategory (ArticleID, CategoryID)
                            VALUES (:article_id, :category_id)
                        """), {'article_id': article_id, 'category_id': category_id})
                        connection.commit()
                        print(f"Inserted ArticleID {article_id} and CategoryID {category_id} into HasCategory.")
                    else:
                        print(f"Skipping insertion into HasCategory as the relationship between ArticleID {article_id} and CategoryID {category_id} already exists.")
                else:
                    print("Skipping insertion into HasCategory as either ArticleID or CategoryID is None.")
        except Exception as e:
            print(f"Error creating table {table_name} or inserting data:\n", e)


    def count(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM Category"))
            return result.scalar()
    
    def get_category_id_for_article(self, article_id):
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT c.CategoryID
                FROM Category c
                JOIN HasCategory hc ON c.CategoryID = hc.CategoryID
                WHERE hc.ArticleID = :article_id
            """), {'article_id': str(article_id)})
            row = result.fetchone()
            if row:
                return row[0]
            return None

    def get_by_id(self, category_id):
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT CategoryID, CategoryName, CategoryLink, ParentCategory
                FROM Category
                WHERE CategoryID = :category_id
            """), {'category_id': category_id})
            row = result.fetchone()
            if row:
                category_id, category_name, category_link, parent_category = row
                return Category(category_id, category_name, category_link, parent_category)
            return None