from rest_framework import permissions, viewsets

from joda_core.models import User
from joda_core.permissions import UserPermission
from joda_core.organization.models import Section, UserGroup
from joda_core.organization.serializers import SectionSerializer, UserSerializer, UserGroupSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('pk')
    permission_classes = (permissions.IsAuthenticated, UserPermission)
    serializer_class = UserSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if self.kwargs[lookup_url_kwarg] == 'me':
            return self.request.user

        return super(UsersViewSet, self).get_object()


class SectionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all().order_by('name')
    serializer_class = SectionSerializer


class UserGroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserGroup.objects.all().order_by('name')
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserGroupSerializer
