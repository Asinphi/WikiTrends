from datetime import datetime

class Article:
    def __init__(self, article_id, title, post_date, last_updated, total_views=None):
        self.article_id = article_id
        self.title = title
        self.post_date = post_date
        self.last_updated = last_updated
        self.total_views = total_views