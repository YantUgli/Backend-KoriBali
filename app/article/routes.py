from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.middleware.role_checker import role_required

from app.article.validation import create_article_schema, update_article_schema, validate
from app.article.service import(
    get_articles_service,
    create_article_service,
    update_article_service,
    delete_article_service,
    add_article_images_service
)

article_blueprint = Blueprint('article', __name__)


@article_blueprint.route('', methods=['get'])
def get_articles():

    result, status = get_articles_service()

    return jsonify(result), status



@article_blueprint.route('', methods=['POST'])
@role_required('member')
def create_article():

    data = request.form.to_dict()

    thumbnailImage = request.files.get('thumbnail_image')

    user_id = get_jwt_identity()

    valid, errors = validate(create_article_schema, data)

    if not valid:
        return jsonify({
            'message' : 'validation error',
            'errors' : errors
        }), 400

    result, status = create_article_service(user_id, data, thumbnailImage)

    return jsonify(result), status



@article_blueprint.route('/<int:article_id>', methods=['PUT'])
@role_required('member')
def update_article(article_id):

    data = request.form.to_dict()

    thumbnailImage = request.files.get('thumbnail_image')

    valid, errors = validate(update_article_schema, data)

    if not valid:
        return jsonify({
            'message' : 'validation error',
            'errors' : errors
        }), 400

    result, status = update_article_service(article_id, data, thumbnailImage)

    return jsonify(result), status



@article_blueprint.route('/<int:article_id>', methods=['DELETE'])
@role_required('member')
def delete_article(article_id):

    result, status = delete_article_service(article_id)

    return jsonify(result), status



@article_blueprint.route('/<int:article_id>/images', methods=['POST'])
def add_article_images(article_id):

    images = request.files.getlist('images')

    return add_article_images_service(article_id, images)


