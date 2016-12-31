import importlib
from django.conf import settings
from rest_framework import routers

from joda_core.router import router as core

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
