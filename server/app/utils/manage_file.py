# import base64
# import io
# import uuid
# import imghdr
import os
from werkzeug.utils import secure_filename

from ..constants import ALLOWED_EXTENSIONS


def allowed_file(filename):
    filename = filename.lower()
    ext = filename.split(".")[-1]
    return ext in ALLOWED_EXTENSIONS


def manage_file(media):
    if allowed_file(media.filename):
        media_name = secure_filename(media.filename)
        media_size = os.fstat(media.fileno()).st_size

        return media_name, media_size
