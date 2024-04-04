from datetime import datetime

class Article:
    def __init__(self, article_id, title, post_date, last_updated):
        self.article_id = article_id
        self.title = title
        self.post_date = post_date
        self.last_updated = last_updated
        self.categories = []

    def add_category(self, category):
        self.categories.append(category)
