from app.repositories.page_view_repository import PageViewRepository
from app.repositories.article_repository import ArticleRepository

class PageViewService:
    def __init__(self, db_config):
        self.page_view_repository = PageViewRepository(db_config)
        self.article_repository = ArticleRepository(db_config)

    async def get_page_views_by_article(self, article_title):
        article = self.article_repository.get_by_title(article_title)
        if article is None:
            return []
        page_views = self.page_view_repository.get_by_article_id(article.article_id)
        return page_views