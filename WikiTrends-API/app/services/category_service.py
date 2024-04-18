from app.repositories.category_repository import CategoryRepository
from app.models.article import Article

class CategoryService:
    def __init__(self, db_config):
        self.category_repository = CategoryRepository(db_config)

    async def get_category_by_article(self, article: Article):
        print(f"Getting category for articleid: {article.article_id}")
        category_id = self.category_repository.get_category_id_for_article(article.article_id)
        if category_id:
            category = self.category_repository.get_by_id(category_id)
            return category
        return None