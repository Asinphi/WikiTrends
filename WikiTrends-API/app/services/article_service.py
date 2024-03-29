from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.utils.wikipedia_api_client import WikipediaAPIClient

class ArticleService:
    @staticmethod
    async def get_article(title):
        article = await ArticleRepository.get_by_title(title)
        if article:
            return article
        # probably wont need this
        article_data = await WikipediaAPIClient.get_article_info(title)
        article = await ArticleRepository.create(article_data)

        categories = article_data.get('categories', [])
        for category_name in categories:
            category = await CategoryRepository.get_by_name(category_name)
            if not category:
                category = await CategoryRepository.create(category_name)
            await article.add_category(category)

        return article
