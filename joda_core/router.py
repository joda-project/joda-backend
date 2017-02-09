from rest_framework import routers

from joda_core import views
from joda_core.documents import views as documents
from joda_core.files import views as files
from joda_core.organization import views as organization

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'authors', views.AuthorsViewSet)
router.register(r'documents', documents.DocumentsViewSet, base_name='documents')
router.register(r'files', files.FilesViewSet, base_name='files')
router.register(r'sections', organization.SectionsViewSet, base_name='sections')
router.register(r'tags', views.TagsViewSet)
router.register(r'users', organization.UsersViewSet, base_name='users')
router.register(r'user-groups', organization.UserGroupsViewSet, base_name='user-groups')
