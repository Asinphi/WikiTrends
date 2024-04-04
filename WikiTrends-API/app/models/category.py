class Category:
    def __init__(self, category_id, category_name, parent_category=None):
        self.category_id = category_id
        self.category_name = category_name
        self.parent_category = parent_category