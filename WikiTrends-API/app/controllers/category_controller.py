from flask import Blueprint, jsonify
from app.services.page_view_service import PageViewService
from config import db_config

page_view_controller = Blueprint("page_view_controller", __name__)

@page_view_controller.route("/articles/<string:article_title>/pageviews", methods=["GET"])
async def get_page_view(article_title):
    page_view_service = PageViewService(db_config)
    page_views = await page_view_service.get_page_views_by_article(article_title)
    return jsonify([page_view.__dict__ for page_view in page_views])