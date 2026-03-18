from flask import current_app
import uuid
import os

def save_image(file):

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    return filepath