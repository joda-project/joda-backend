import importlib
from django.conf import settings
from rest_framework import permissions, response, routers
from rest_framework.decorators import api_view, permission_classes

from joda.version import get_version
from joda_core.router import router as core


@api_view()
@permission_classes((permissions.AllowAny,))
def about_view(_):
    out = {
        'version': get_version(),
        'features': {}
    }

    for feature in settings.JODA_FEATURES:
        if not 'joda_' in feature:
            feature = 'joda_' + feature

        module = importlib.import_module(feature)
        out['features'][feature] = {
            'version': module.version
        }

    return response.Response(out)


class JodaRouter(routers.DefaultRouter):

    def extend(self, router):
        self.registry.extend(router.registry)

    def add_features(self):
        self.extend(core)

        for feature in settings.JODA_FEATURES:
            if not 'joda_' in feature:
                feature = 'joda_' + feature

            module = importlib.import_module('.router', feature)
            self.extend(module.router)
