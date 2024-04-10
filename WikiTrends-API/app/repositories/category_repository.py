# category_repository.py
from sqlalchemy import text
from app.models.category import Category

class CategoryRepository:
    def __init__(self, engine):
        self.engine = engine
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        table_name = 'Categories'
        table = f"""
            BEGIN
                EXECUTE IMMEDIATE 'CREATE TABLE {table_name} (
                    CategoryID INTEGER PRIMARY KEY,
                    CategoryName VARCHAR2(255) NOT NULL,
                    ParentCategory INTEGER
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
                EXECUTE IMMEDIATE 'CREATE SEQUENCE Categories_seq
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
            result = conn.execute(text("SELECT CategoryID, CategoryName, ParentCategory FROM Categories WHERE CategoryName = :category_name"), {'category_name': category_name})
            row = result.fetchone()
            if row:
                category_id, category_name, parent_category = row
                return Category(category_id, category_name, parent_category)
            return None

    def create(self, category):
        with self.engine.connect() as conn:
            try:
                result = conn.execute(text("SELECT CategoryID FROM Categories WHERE CategoryName = :category_name"), {'category_name': category.category_name})
                if result.fetchone() is None:
                    conn.execute(text("""
                        INSERT INTO Categories (CategoryID, CategoryName, ParentCategory)
                        VALUES (Categories_seq.NEXTVAL, :category_name, :parent_category)
                    """), {'category_name': category.category_name, 'parent_category': category.parent_category})
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
                    PRIMARY KEY (ArticleID, CategoryID)
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
                
                result = connection.execute(text("SELECT ArticleID, CategoryID FROM HasCategory WHERE ArticleID = :article_id AND CategoryID = :category_id"), {'article_id': article_id, 'category_id': category_id})
                if result.fetchone() is None:
                    connection.execute(text("""
                        INSERT INTO HasCategory (ArticleID, CategoryID)
                        VALUES (:article_id, :category_id)
                    """), {'article_id': article_id, 'category_id': category_id})
                    connection.commit()
                else:
                    print(f"Article-Category relationship already exists for ArticleID {article_id} and CategoryID {category_id}.")
        except Exception as e:
            print(f"Error creating table {table_name} or inserting data:\n", e)