"""
Joda Backend URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from joda.helpers import DefaultRouter
from joda_core.router import router as core

router = DefaultRouter(trailing_slash=False)
router.extend(core)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
