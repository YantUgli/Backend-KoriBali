import os
from PIL import Image
from uuid import uuid4

BASE_UPLOAD_PATH = "uploads/articles"

def generate_filename(extension):
    return f"{uuid4().hex}.{extension}"

def save_image_version(file):

    img = Image.open(file)

    # ensure format
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    ext = file.filename.rsplit('.', 1)[-1].lower()
    filename = generate_filename(ext)

    # path
    original_path = os.path.join(BASE_UPLOAD_PATH, "original", filename)
    medium_path = os.path.join(BASE_UPLOAD_PATH, "medium", filename)
    thumbnail_path = os.path.join(BASE_UPLOAD_PATH, "thumbnail", filename)

    # save original
    img.save(original_path, optimize=True, quality=95)


    # save medium
    medium = img.copy() 
    medium.thumbnail((800, 800))
    medium.save(medium_path, optimize=True)

    # save thumbnail
    thumb = img.copy()
    thumb.thumbnail((300, 300))
    thumb.save(thumbnail_path, optimized=True, quality=75)

    return{
        "original" : original_path,
        "medium": medium_path,
        "thumbnail" : thumbnail_path
    }