"""
Joda Backend URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from joda.helpers import JodaRouter

router = JodaRouter(trailing_slash=False)
router.add_features()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
