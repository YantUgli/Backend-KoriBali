from flask import current_app
from app.extensions import db
from werkzeug.utils import secure_filename
import os 
import uuid

from app.article.models import Article, ArticleImages
from app.utils.image_handler import save_image

# pakai image processing
from app.utils.image_processor import save_image_version



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
    # old
    # thumbnailImage.save(filepath)

    paths = save_image_version(thumbnailImage)

    article = Article(
        title=data.get('title'),
        description=data.get('description'),
        user_id=user_id,
        thumbnail_path=paths["medium"]  # pilih medium buat thumbnail utama
    )

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
        # old
        # if article.thumbnail_path and os.path.exists(article.thumbnail_path):
        #         os.remove(article.thumbnail_path)

        # filepath = save_image(thumbnailImage)

        # article.thumbnail_path = filepath

        # new
        paths = save_image_version(thumbnailImage)
        article.thumbnail_path = paths["medium"]

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
        # old
        # filepath = save_image(image)

        # image = ArticleImages(
        #     article_id = article_id,
        #     image_url = filepath
        # )
        
        # new
        paths = save_image_version(image)

        image = ArticleImages(
            article_id=article_id,
            original_url=paths["original"],
            medium_url=paths["medium"],
            thumbnail_url=paths["thumbnail"]
        )


        db.session.add(image)
        saved.append(paths)

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
    
    # old
    # old_path = articleImage.image_url

    # if os.path.exists(old_path):
    #     os.remove(old_path)

    # new
    
    paths = [
    articleImage.original_url,
    articleImage.medium_url,
    articleImage.thumbnail_url
]

    for path in paths:
        if path and os.path.exists(path):
            os.remove(path)

    db.session.delete(articleImage)
    db.session.commit()

    return {
        'message' : 'delete image successfully'
    }, 200