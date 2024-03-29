from flask import Blueprint, jsonify
from app.services.article_service import ArticleService

article_controller = Blueprint("article_controller", __name__)

@article_controller.route("/articles/<string:article_title>", methods=["GET"])
async def get_article(article_title):
    article_service = ArticleService(db_config)
    article = await article_service.get_article(article_title)
    return jsonify(article.__dict__)
