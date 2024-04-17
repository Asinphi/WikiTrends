from app.repositories.user_search_repository import UserSearchRepository

class UserSearchService:
    def __init__(self, db_config):
        self.user_search_repository = UserSearchRepository(db_config)
        self.user_search_repository.create_search_results_view()

    async def get_user_search_by_term(self, search_term):
        user_search = self.user_search_repository.get_by_search_term(search_term)
        return user_search