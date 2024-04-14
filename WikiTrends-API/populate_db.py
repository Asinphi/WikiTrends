import asyncio
from app.utils.wikipedia_api_client import WikipediaAPIClient
from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.page_view_repository import PageViewRepository
from app.repositories.user_search_repository import UserSearchRepository
from app.models.article import Article
from app.models.category import Category
from app.models.page_view import PageView
from app.models.user_search import UserSearch
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from config import Config

async def populate_database():
    db_config = Config.SQLALCHEMY_DATABASE_URI
    engine = create_engine(db_config)
    
    article_repository = ArticleRepository(engine)
    category_repository = CategoryRepository(engine)
    page_view_repository = PageViewRepository(engine)
    user_search_repository = UserSearchRepository(engine)
    
    wikipedia_api_client = WikipediaAPIClient()
    
    articles = await wikipedia_api_client.get_articles()
    try:
        for article_title in articles:
            article_info = await wikipedia_api_client.get_article_info(article_title)
            
            if article_info:
                article = Article(
                    None,
                    article_info["title"],
                    datetime.strptime(article_info["post_date"], "%Y-%m-%dT%H:%M:%SZ"),
                    datetime.strptime(article_info["last_updated"], "%Y-%m-%dT%H:%M:%SZ")
                )
                article_id = article_repository.create(article)

                if article_id:
                    for category_info in article_info["categories"]:
                        category = category_repository.get_by_name(category_info["category_name"])
                        if not category:
                            category = Category(None, category_info["category_name"], category_info["category_link"], None)
                            category_id = category_repository.create(category)
                        else:
                            category_id = category.category_id
                        
                        category_repository.add_article_category(article_id, category_id)
                    
                    end_date = datetime.now().strftime("%Y%m%d")
                    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
                    page_views_df = await wikipedia_api_client.get_article_pageviews(article_title, start_date, end_date)
                    
                    if page_views_df is not None:
                        for _, row in page_views_df.iterrows():
                            page_view = PageView(
                                article_id,
                                datetime.strptime(row["view_date"][:8], "%Y%m%d"),
                                row["view_count"]
                            )
                            try:
                                page_view_repository.create(page_view)
                            except Exception as e:
                                print(f"Error inserting page view into database:\n {e}")
                    
                    user_search = UserSearch(None, datetime.now(), article_title)
                    user_search_repository.create(user_search)
    except Exception as e:
        print(f"An error occurred during database population: {e}")

if __name__ == "__main__":
    asyncio.run(populate_database())