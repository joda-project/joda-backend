"""Global Joda router"""

import importlib
from rest_framework import routers

from joda.helpers import features
from joda_core.router import router as core


class JodaRouter(routers.DefaultRouter):
    """Improved API router for simpler extension"""

    def extend(self, router):
        """Extend this router with existing router"""
        self.registry.extend(router.registry)

    def add_features(self):
        """Add all loaded Joda features to router"""
        self.extend(core)

        features_dict = features()
        for feature in features_dict:
            module = importlib.import_module(
                '.router', features_dict[feature]['module'])
            self.extend(module.router)
