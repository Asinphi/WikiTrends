from app.repositories.article_repository import ArticleRepository
from app.utils.wikipedia_api_client import WikipediaAPIClient

class ArticleService:
    def __init__(self, db_config):
        self.article_repository = ArticleRepository(db_config)
        self.wikipedia_api_client = WikipediaAPIClient()
        
        

    async def get_article(self, article_title):
        article = self.article_repository.get_by_title(article_title)
        if article is None:
            article_info = await self.wikipedia_api_client.get_article_info(article_title)
            article = Article(
                article_id=None,
                title=article_info["title"],
                post_date=article_info["post_date"],
                last_updated=article_info["last_updated"]
            )
            self.article_repository.create(article)
        return article

    async def get_article_pageviews(self, article_title, start_date, end_date):
        pageviews_data = await self.wikipedia_api_client.get_article_pageviews(article_title, start_date, end_date)
        return pageviews_data
    
    async def get_long_lost_article(self):
        
        article = self.article_repository.create_long_lost_articles_view()
        return article

    async def get_top_three_articles(self, date):
        articles = self.article_repository.create_top_three_view(date)
        
        return articles
