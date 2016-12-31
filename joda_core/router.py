from rest_framework import routers

from joda_core import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'authors', views.AuthorsViewSet)
router.register(r'contents', views.ContentsViewSet)
router.register(r'files', views.FilesViewSet)
router.register(r'tags', views.TagsViewSet)
router.register(r'users', views.UsersViewSet, base_name='users')
