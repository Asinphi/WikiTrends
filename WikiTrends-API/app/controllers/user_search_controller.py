from flask import Blueprint, jsonify
from app.services.user_search_service import UserSearchService
from config import db_config

user_search_controller = Blueprint("user_search_controller", __name__)

@user_search_controller.route("/searches/<string:search_term>", methods=["GET"])
def get_user_search(search_term):
    user_search_service = UserSearchService(db_config)
    user_search_service.insert_user_search(search_term)
    articles = user_search_service.get_search_results(search_term)
    print(f"Retrieved articles for search term: {search_term}")
    for article in articles:
        print(f"Article: {article.title}")
    return jsonify([article.__dict__ for article in articles]), 200