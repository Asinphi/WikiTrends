from flask import Blueprint, jsonify, request
from app.services.article_service import ArticleService
from config import db_config

article_controller = Blueprint("article_controller", __name__)

@article_controller.route("/articles/<string:article_title>", methods=["GET"])
async def get_article(article_title):
    article_service = ArticleService(db_config)
    article = await article_service.get_article(article_title)
    if article:
        print(f"Retrieved article: {article}")
        return jsonify(article.__dict__)
    else:
        print(f"No article found with title: {article_title}")
        return jsonify({"message": "Article not found."}), 404

@article_controller.route("/articles/<string:article_title>/pageviews", methods=["GET"])
async def get_article_pageviews(article_title):
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    article_service = ArticleService(db_config)
    pageviews = await article_service.get_article_pageviews(article_title, start_date, end_date)
    if pageviews.empty:
        print(f"No pageviews found for article: {article_title}, start_date: {start_date}, end_date: {end_date}")
        return jsonify({"message": "No pageviews found for the specified article and date range."}), 404
    else:
        print(f"Retrieved pageviews for article: {article_title}, start_date: {start_date}, end_date: {end_date}")
        return jsonify(pageviews.to_dict(orient="records"))

@article_controller.route("/long-lost-article", methods=["GET"])
async def get_long_lost_article():
    article_service = ArticleService(db_config)
    article = await article_service.get_long_lost_article()
    if article:
        print(f"Retrieved long-lost article: {article}")
        return jsonify(article.__dict__)
    else:
        print("No long-lost article found.")
        return jsonify({"message": "No long-lost article found."}), 404

@article_controller.route("/top-three-articles", methods=["GET"])
async def get_top_three_articles():
    date = request.args.get("date")
    article_service = ArticleService(db_config)
    articles = await article_service.get_top_three_articles(date)
    if articles:
        print(f"Retrieved top three articles for date: {date}")
        return jsonify([article.__dict__ for article in articles])
    else:
        print(f"No top three articles found for date: {date}")
        return jsonify({"message": "No top three articles found for the specified date."}), 404
