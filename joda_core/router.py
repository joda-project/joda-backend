from rest_framework import routers

from joda_core.views import common, files

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'authors', common.AuthorsViewSet)
router.register(r'contents', common.ContentsViewSet)
router.register(r'files', files.FilesViewSet)
router.register(r'tags', common.TagsViewSet)
router.register(r'users', common.UsersViewSet, base_name='users')
