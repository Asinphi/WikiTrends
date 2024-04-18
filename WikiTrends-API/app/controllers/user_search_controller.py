from flask import Blueprint, jsonify
from app.services.user_search_service import UserSearchService
from config import db_config

user_search_controller = Blueprint("user_search_controller", __name__)

@user_search_controller.route("/searches/<string:search_term>", methods=["GET"])
async def get_user_search(search_term):
    user_search_service = UserSearchService(db_config)
    user_search = await user_search_service.get_search_results(search_term)
    return jsonify(user_search.__dict__)