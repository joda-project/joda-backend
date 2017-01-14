from rest_framework import routers

from joda_core import views
from joda_core.content import views as content
from joda_core.files import views as files

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'authors', views.AuthorsViewSet)
router.register(r'contents', content.ContentsViewSet, base_name='contents')
router.register(r'files', files.FilesViewSet, base_name='files')
router.register(r'tags', views.TagsViewSet)
router.register(r'users', views.UsersViewSet, base_name='users')
