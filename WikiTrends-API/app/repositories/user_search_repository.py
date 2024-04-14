from sqlalchemy import text
from app.models.user_search import UserSearch

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

    def get_by_search_term(self, search_term):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT SearchID, SearchDate, SearchTerm FROM UserSearch WHERE SearchTerm = :search_term"), {'search_term': search_term})
            row = result.fetchone()
            if row:
                search_id, search_date, search_term = row
                return UserSearch(search_id, search_date, search_term)
            return None

    def create(self, user_search):
        with self.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO UserSearch (SearchID, SearchDate, SearchTerm)
                VALUES (UserSearch_seq.NEXTVAL, :search_date, :search_term)
            """), {'search_date': user_search.search_date, 'search_term': user_search.search_term})
            conn.commit()
            print(f"Inserted user search for term '{user_search.search_term}' on {user_search.search_date}.")