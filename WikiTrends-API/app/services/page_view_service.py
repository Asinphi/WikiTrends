from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.utils.wikipedia_api_client import WikipediaAPIClient

class ArticleService:
    @staticmethod
    async def get_page_view(title):
        page_view = await PageViewRepository.get_by_title(title)
        if page_view:
            return page_view
        # probably wont need this
        page_view_data = await WikipediaAPIClient.get_page_view_info(title)
        page_view = await PageViewRepository.create(page_view_data)

        categories = page_view_data.get('categories', [])
        for category_name in categories:
            category = await CategoryRepository.get_by_name(category_name)
            if not category:
                category = await CategoryRepository.create(category_name)
            await page_view.add_category(category)

        return page_view
