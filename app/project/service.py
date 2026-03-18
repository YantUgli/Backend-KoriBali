from flask import current_app
from app.models.project import Project
from app.models.project_images import ProjectImages
from app.extensions import db

from werkzeug.utils import secure_filename
import os
import uuid
from app.utils.image_handler import save_image 



def get_projects_service():

    projects = Project.query.all()

    result = [project.to_dict() for project in projects]

    return result, 200



def create_project_service(data, thumbnailImage):
    
    if not thumbnailImage:
        return {
            'message': 'thumbnail image is required'
        }, 400
    
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

    return {
        'message' : 'project created successfully',
        'data' : project.to_dict()
    }, 201



def update_project_service(project_id, data, thumbnailImage):
    
    project = Project.query.get(project_id)

    if not project:
        return {
            "message": "project not found"
        }, 404
    
    if not thumbnailImage:
        return {
            'message' : 'thumbnail image is required'
        }, 400

    upload_folder = current_app.config['UPLOAD_FOLDER']

    # extract extension gambarnya 
    ext = thumbnailImage.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(upload_folder, filename)

    thumbnailImage.save(filepath)
    
    # Delete old thumbnail
    if project.thumbnail_path:
        old_path= project.thumbnail_path
        if os.path.exists(old_path):
            os.remove(old_path)

    project.title = data.get('title')
    project.description = data.get('description')
    project.type = data.get('type') 
    project.thumbnail_path = filepath

    db.session.commit()

    return {
        'message' : 'project update successfully',
        'data' : project.to_dict()
    }, 200



def delete_project_service(project_id):

    project = Project.query.get(project_id)

    if not project:
        return {
            'message' : 'project not found'
        }, 404
    
    try:
        db.session.delete(project)
        db.session.commit()

        return {
            'message' : 'delete project successfully'
        }, 200
    except Exception as e: 
        db.session.rollback()
        return {
            'message' : 'error accur the process',
            'error' : str(e)
        }, 400
    


def add_project_images_service(project_id, images):

    project = Project.query.get(project_id)

    if not project:
        return {"message": "project not found"}, 404

    saved = []

    for img in images:

        filepath = save_image(img)

        image = ProjectImages(
            project_id=project_id,
            image_url=filepath
        )

        db.session.add(image)
        saved.append(filepath)

    db.session.commit()

    return {
        "message": "images uploaded",
        "images": saved
    }, 201



def delete_image_project_service(project_image_id):

    projectImage = ProjectImages.query.get(project_image_id)

    if not projectImage:
        return {
            'message' : 'project not found'
        }, 404
    
    old_path = projectImage.image_url

    if os.path.exists(old_path):
        os.remove(old_path)

    
    db.session.delete(projectImage)
    db.session.commit()

    return {
        'message' : 'delete image successfully'
    }, 200