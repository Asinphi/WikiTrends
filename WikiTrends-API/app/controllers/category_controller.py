from flask import Blueprint, jsonify
from app.services.category_service import CategoryService
from config import db_config

category_controller = Blueprint("category_controller", __name__)

@category_controller.route("/categories/<string:category_name>", methods=["GET"])
async def get_category(category_name):
    category_service = CategoryService(db_config)
    category = await category_service.get_category_by_name(category_name)
    return jsonify(category.__dict__)