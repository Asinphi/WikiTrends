from flask import Flask
from app.controllers.article_controller import article_controller
from app.controllers.page_view_controller import page_view_controller
from app.controllers.user_search_controller import user_search_controller
from app.controllers.category_controller import category_controller
from config import db_config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_config.url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(article_controller)
app.register_blueprint(page_view_controller)
app.register_blueprint(user_search_controller)
app.register_blueprint(category_controller)

if __name__ == "__main__":
    app.run(debug=True)