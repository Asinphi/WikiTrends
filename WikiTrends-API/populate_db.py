# populate_db.py
import asyncio
import aiohttp
from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.page_view_repository import PageViewRepository
from app.repositories.user_search_repository import UserSearchRepository
from app.models.article import Article
from app.models.category import Category
from app.models.page_view import PageView
from app.models.user_search import UserSearch
from app.utils.wikipedia_api_client import WikipediaAPIClient
from config import db_config

async def populate_database():
    article_repository = ArticleRepository(db_config)
    category_repository = CategoryRepository(db_config)
    page_view_repository = PageViewRepository(db_config)
    user_search_repository = UserSearchRepository(db_config)
    wikipedia_api_client = WikipediaAPIClient()

    random_articles = await wikipedia_api_client.get_random_articles()
    processed_articles = set()

    async with aiohttp.ClientSession() as session:
        for article_title in random_articles:
            if article_title in processed_articles:
                continue
            processed_articles.add(article_title)

            article_info = await wikipedia_api_client.get_article_info(article_title)
            if article_info is None:
                continue

            article = Article(
                article_id=None,
                title=article_info["title"],
                post_date=article_info["post_date"],
                last_updated=article_info["last_updated"]
            )
            article_repository.create(article)

            for category_name in article_info["categories"]:
                category = category_repository.get_by_name(category_name)
                if category is None:
                    category = Category(category_id=None, category_name=category_name, parent_category=None)
                    category_repository.create(category)
                category_repository.add_article_category(article.article_id, category.category_id)

            pageviews_data = await wikipedia_api_client.get_article_pageviews(article_title, "2023010100", "2023053100")
            if pageviews_data is not None:
                for _, row in pageviews_data.iterrows():
                    page_view = PageView(
                        article_id=article.article_id,
                        view_date=row["timestamp_"],
                        view_count=row["view_count"]
                    )
                    page_view_repository.create(page_view)

            user_search = UserSearch(
                search_id=None,
                search_date="2023-05-31",
                search_term=article_title
            )
            user_search_repository.create(user_search)

if __name__ == "__main__":
    asyncio.run(populate_database())