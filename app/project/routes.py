from flask import Blueprint, request, jsonify, current_app
from app.models.project import Project
from werkzeug.utils import secure_filename
import uuid
import os

from app.extensions import db

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('', methods=['GET'])
def get_projects():
    projects = Project.query.all()

    result = [project.to_dict() for project in projects]

    return jsonify(result), 200



@project_blueprint.route('', methods=['POST'])
def create_project():

    data = request.form.to_dict()
    thumbnailImage = request.files.get('thumbnail_image')

    if not thumbnailImage:
        return jsonify({
            'message': 'thumbnail image is required'
        }), 400
    
    upload_folder = current_app.config['UPLOAD_FOLDER']

    # extract extension gambarnya 
    ext = thumbnailImage.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(upload_folder, filename)

    thumbnailImage.save(filepath)

    project = Project(
        title=data.get('title'),
        description = data.get('description'),
        type = data.get('type'),
        thumbnail_path = filepath
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({
        'message' : 'project created successfully',
        'data' : project.to_dict()
    }), 201



@project_blueprint.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):

    project = Project.query.get(project_id)

    if not project:
        return jsonify({
            "message": "project not found"
        }), 404
    
    data = request.form.to_dict()

    thumbnailImage = request.files.get('thumbnail_image')

    if thumbnailImage:
        upload_folder = current_app.config['UPLOAD_FOLDER']

        # extract extension gambarnya 
        ext = thumbnailImage.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        filepath = os.path.join(upload_folder, filename)

        thumbnailImage.save(filepath)
        
        project.title = data.get('title')
        project.description = data.get('description')
        project.type = data.get('type') 
        project.thumbnail_path = filepath

    db.session.commit()

    return jsonify({
        'message' : 'project update successfully',
        'data' : project.to_dict()
    }), 200



@project_blueprint.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):

    project = Project.query.get(project_id)

    if not project:
        return jsonify({
            'message' : 'project not found'
        }), 404
    
    try:
        db.session.delete(project)
        db.session.commit()

        return jsonify({
            'message' : 'delete project successfully'
        }), 200
    except Exception as e: 
        db.session.rollback()
        return jsonify({
            'message' : 'error accur the process',
            'error' : str(e)
        }), 400