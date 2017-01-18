import hashlib
import os
import sys

from datetime import datetime
from django.utils.lru_cache import lru_cache
from rest_framework import exceptions, status

from joda_core.files.models import File


@lru_cache()
def upload_path():
    return os.environ['FILES_UPLOAD_PATH']


class FileIOException(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'I/O error when processing the file'
    default_code = 'file_io'


def get_md5(file):
    hash_md5 = hashlib.md5()
    try:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    except IOError as exception:
        print(exception, file=sys.stderr)
        raise FileIOException
    return hash_md5.hexdigest()


def get_size(name):
    path = upload_path()
    statinfo = os.stat(os.path.join(path, name))
    return statinfo.st_size


def handle_uploaded_file(file, file_type):
    created_at = datetime.now()
    md5 = get_md5(file)
    name = md5 + '_' + str(int(created_at.timestamp())) + File.get_extension(file_type)

    path = upload_path()
    try:
        with open(os.path.join(path, name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except IOError as exception:
        print(exception, file=sys.stderr)
        raise FileIOException

    size = get_size(name)

    return md5, created_at, size
