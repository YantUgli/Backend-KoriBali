from flask import current_app
from app.extensions import db
from werkzeug.utils import secure_filename
import os 
import uuid

from app.models.article import Article
from app.models.article_image import ArticleImages
from app.utils.image_handler import save_image



def get_articles_service():
    
    articles = Article.query.all()

    result = [article.to_dict() for article in articles]

    return result, 200



def create_article_service(user_id, data, thumbnailImage):
    
    if not thumbnailImage:
        return {
            'message' : 'thumbnail image is required'
        }, 400
    
    upload_folder = current_app.config['UPLOAD_FOLDER']

    ext = thumbnailImage.filename.split('.')[-1]

    filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(upload_folder, filename)

    thumbnailImage.save(filepath)

    article = Article(
        title = data.get('title'),
        description = data.get('description'),
        user_id = user_id,
        thumbnail_path = filepath
    )

    db.session.add(article)
    db.session.commit()

    return {
        'message': 'article created successfully',
        'data' : article.to_dict()
    }, 201



def update_article_service(article_id, data, thumbnailImage):
    
    article = Article.query.get(article_id)

    if not article:
        return {
            'message' : 'article not found'
        }, 404
    
    # sudah ada validation jadi tidak perlu lagi
    # if data.get('title'):
    #     article.title = data.get('title') 

    # if data.get('description'):
    #     article.description = data.get('description')


    if thumbnailImage:

        if article.thumbnail_path and os.path.exists(article.thumbnail_path):
                os.remove(article.thumbnail_path)

        filepath = save_image(thumbnailImage)

        article.thumbnail_path = filepath

    db.session.commit()

    return {
        'message' : 'article updated successfully',
        'data' : article.to_dict()
    }, 200


def delete_article_service(article_id):
    
    article = Article.query.get(article_id)

    if not article:
        return {
            'message' : 'article not found'
        }, 404
    
    try:
        db.session.delete(article)
        db.session.commit()

        return {
            'message' : 'remove data article successfully'
        }, 200

    except Exception as e:
        db.session.rollback()

        return {
            'message' : 'error occur the process',
            'error' : str(e)
        },400



def add_article_images_service(article_id, images):

    article = Article.query.get(article_id)

    if not article:
        return {'message' : 'article not found'}, 404
    
    if not images:
        return {'message' : 'images is not found'}, 404

    saved = []

    for image in images:
        
        filepath = save_image(image)

        image = ArticleImages(
            article_id = article_id,
            image_url = filepath
        )

        db.session.add(image)
        saved.append(filepath)

    db.session.commit()

    return {
        'message' : 'images uploaded'
    }, 201



def delete_image_article_service(article_image_id):

    articleImage = ArticleImages.query.get(article_image_id)

    if not articleImage:
        return {
            'message' : 'article not found'
        }, 404
    
    old_path = articleImage.image_url

    if os.path.exists(old_path):
        os.remove(old_path)

    db.session.delete(articleImage)
    db.session.commit()

    return {
        'message' : 'delete image successfully'
    }, 200