"""
Django settings for joda project - devel
"""

from joda.settings import *

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS += [
    'joda_misc'
]

JODA_FEATURES += [
    'misc'
]

X_FRAME_OPTIONS = ''
