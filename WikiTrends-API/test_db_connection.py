import logging
from flask import Flask
from config import Config
from sqlalchemy import create_engine, text
from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.page_view_repository import PageViewRepository
from app.repositories.user_search_repository import UserSearchRepository
from app.models.article import Article
from app.models.category import Category
from app.models.page_view import PageView
from app.models.user_search import UserSearch
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object(Config)


def test_repositories():
    try:
        db_config = app.config['SQLALCHEMY_DATABASE_URI']
        logging.debug(f"Database connection string: {db_config}")

        engine = create_engine(db_config)
        with engine.connect() as connection:
            logging.debug("Connected to Oracle database successfully!")
            logging.debug(f"Database version: {connection.dialect.server_version_info}")
            logging.debug("Running repository tests...")

             # Test ArticleRepository
            article_repository = ArticleRepository(engine)
            article = Article(None, 'Test Article', datetime.now(), datetime.now())
            try:
                article_id = article_repository.create(article)
                retrieved_article = article_repository.get_by_title('Test Article')
                assert retrieved_article.title == 'Test Article'
                logging.debug("ArticleRepository tests passed successfully!")
            except Exception as e:
                logging.error(f"Error during ArticleRepository tests: {e}")


            logging.debug("ArticleRepository tests passed successfully!")  
            logging.debug("Running CategoryRepository tests...")
            # Test CategoryRepository
            category_repository = CategoryRepository(engine)
            category = Category(None, 'Test Category', None)
            category_repository.create(category)
            retrieved_category = category_repository.get_by_name('Test Category')
            assert retrieved_category.category_name == 'Test Category'
            category_repository.add_article_category(article_id, retrieved_category.category_id)

            logging.debug("CategoryRepository tests passed successfully!")
            logging.debug("Running PageViewRepository tests...")

            # Test PageViewRepository
            page_view_repository = PageViewRepository(engine)
            page_view = PageView(article_id, datetime.now(), 100)
            page_view_repository.create(page_view)
            retrieved_page_views = page_view_repository.get_by_article_id(article_id)
            assert len(retrieved_page_views) > 0

            logging.debug("PageViewRepository tests passed successfully!")
            logging.debug("Running UserSearchRepository tests...")
            # Test UserSearchRepository
            user_search_repository = UserSearchRepository(engine)
            user_search = UserSearch(None, datetime.now(), 'Test Search')
            user_search_repository.create(user_search)
            retrieved_user_search = user_search_repository.get_by_search_term('Test Search')
            assert retrieved_user_search.search_term == 'Test Search'

            logging.debug("All repository tests passed successfully!")

    except Exception as e:
        logging.error(f"Error during repository tests: {e}")

if __name__ == "__main__":
    test_repositories()