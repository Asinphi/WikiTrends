from app.repositories.user_search_repository import UserSearchRepository

class UserSearchService:
    def __init__(self, db_config):
        self.user_search_repository = UserSearchRepository(db_config)
        
    def insert_user_search(self, search_term):
        user_search = UserSearch(search_date=datetime.now(), search_term=search_term)
        self.user_search_repository.create(user_search)

    def get_search_results(self, search_term):
        search_results = self.user_search_repository.get_search_results(search_term)
        print(f"Retrieved search results: {search_results}")
        return search_results