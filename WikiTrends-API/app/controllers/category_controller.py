from flask import Blueprint, jsonify
from app.services.category_service import CategoryService
from config import db_config
from app.repositories.article_repository import ArticleRepository

category_controller = Blueprint("category_controller", __name__)

@category_controller.route("/categories/<string:article_title>", methods=["GET"])
async def get_category(article_title):
    article_repository = ArticleRepository(db_config)
    article = article_repository.get_by_title(article_title)

    if article:
        category_service = CategoryService(db_config)
        category = await category_service.get_category_by_article(article)
        if category:
            return jsonify(category.__dict__)
        else:
            return jsonify({"error": "Category not found"}), 404
    else:
        return jsonify({"error": "Article not found"}), 404