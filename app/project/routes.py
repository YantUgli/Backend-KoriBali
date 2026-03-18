from flask import Blueprint, request, jsonify

from app.extensions import db
from app.project.service import (
    get_projects_service,
    create_project_service,
    update_project_service,
    delete_project_service,
    add_project_images_service,
    delete_image_project_service
    )

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('', methods=['GET'])
def get_projects():

    result, status = get_projects_service()

    return jsonify(result), status



@project_blueprint.route('', methods=['POST'])
def create_project():

    data = request.form.to_dict()
    thumbnailImage = request.files.get('thumbnail_image')

    result, status = create_project_service(data, thumbnailImage)

    return jsonify(result), status



@project_blueprint.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):

    data = request.form.to_dict()

    thumbnailImage = request.files.get('thumbnail_image')

    result, status = update_project_service(project_id, data, thumbnailImage)

    return jsonify(result), status



@project_blueprint.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):

    result, status = delete_project_service(project_id)

    return jsonify(result), status



@project_blueprint.route('/<int:project_id>/images', methods=['POST'])
def add_project_images(project_id):

    images = request.files.getlist('images')

    return add_project_images_service(project_id, images)



@project_blueprint.route('/image/<int:project_image_id>', methods=['DELETE'])
def delete_image_project(project_image_id):

    result, status = delete_image_project_service(project_image_id)

    return jsonify(result), status