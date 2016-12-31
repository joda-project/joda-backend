"""
WSGI config for Joda Backend
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "joda.settings")

application = get_wsgi_application()
