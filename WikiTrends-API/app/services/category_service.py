from app.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db_config):
        self.category_repository = CategoryRepository(db_config)

    async def get_category_by_name(self, category_name):
        category = self.category_repository.get_by_name(category_name)
        return category