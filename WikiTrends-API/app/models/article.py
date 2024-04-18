from datetime import datetime

class Article:
    def __init__(self, title, total_views=None, article_id=None, post_date=None, last_updated=None):
        self.article_id = article_id
        self.title = title
        self.post_date = post_date
        self.last_updated = last_updated
        self.total_views = total_views
