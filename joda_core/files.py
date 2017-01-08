import hashlib
import os
import sys
import time

from django.utils.lru_cache import lru_cache

from rest_framework import exceptions, status


@lru_cache()
def upload_path():
    return os.environ['FILES_UPLOAD_PATH']


class FileIOException(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'I/O error when processing the file'
    default_code = 'file_io'


def sanitize_name(string):
    return ''.join(c for c in string if c.isalnum() or c in '.-_').strip()


def get_unique_name(name):
    if not name:
        name = 'upload-{}.pdf'.format(int(time.time()))

    prefix, extension = os.path.splitext(name)
    if not extension:
        extension = '.pdf'

    path = upload_path()
    name = sanitize_name(prefix + extension.lower())
    fullname = os.path.join(path, name)
    index = 1
    while os.path.exists(fullname):
        name = prefix + '-' + str(index) + extension.lower()
        fullname = os.path.join(path, name)
        index = index + 1
    return name


def get_md5(name):
    path = upload_path()
    hash_md5 = hashlib.md5()
    try:
        with open(os.path.join(path, name), "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except IOError as exception:
        print(exception, file=sys.stderr)
        raise FileIOException
    return hash_md5.hexdigest()


def handle_uploaded_file(file):
    name = get_unique_name(file.name)
    path = upload_path()
    try:
        with open(os.path.join(path, name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except IOError as exception:
        print(exception, file=sys.stderr)
        raise FileIOException

    md5 = get_md5(name)
    return name, md5
