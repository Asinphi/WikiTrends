from flask import Blueprint, jsonify
from app.services.user_search_service import UserSearchService
from config import db_config

user_search_controller = Blueprint("user_search_controller", __name__)

@user_search_controller.route("/searches/<string:search_term>", methods=["GET"])
def get_user_search(search_term):
    user_search_service = UserSearchService(db_config)
    user_search_service.insert_user_search(search_term)
    search_results = user_search_service.get_search_results(search_term)
    print(f"Retrieved search results for search term: {search_term}")
    for result in search_results:
        article = result['article']
        page_views = result['page_views']
        print(f"Article: {article.title}")
        for page_view in page_views:
            print(f"  - View Date: {page_view.view_date}, View Count: {page_view.view_count}, Sum: {article.total_views}")
    return jsonify([{
        'article': {'title': result['article'].title},
        'page_views': [{'view_date': page_view.view_date, 'view_count': page_view.view_count} for page_view in result['page_views']]
    } for result in search_results]), 200