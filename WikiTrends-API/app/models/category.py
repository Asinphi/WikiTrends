class Category:
    def __init__(self, category_id, category_name, category_link, parent_category=None):
        self.category_id = category_id
        self.category_name = category_name
        self.category_link = category_link
        self.parent_category = parent_category