"""Global Joda helper functions and classes"""

import importlib
from django.conf import settings
from django.utils.lru_cache import lru_cache
from rest_framework import permissions, response, routers
from rest_framework.decorators import api_view, permission_classes

from joda import version_string
from joda.version import get_version
from joda_core.router import router as core


@lru_cache()
def features():
    """Returns a dictionary of features and their properties."""
    features_dict = {}

    for feature in settings.JODA_FEATURES:
        if 'joda_' in feature:
            feature = feature[5:]

        module_name = 'joda_' + feature
        module = importlib.import_module(module_name)
        features_dict[feature] = {
            'module': module_name,
            'version': get_version(module.VERSION, module.module_path),
            'model_name': module.model_name,
            'item_name': module.item_name,
            'item_group': module.item_group
        }

    return features_dict


@api_view()
@permission_classes((permissions.AllowAny,))
def about_view(_):
    """Simple about API view"""
    out = {
        'version': version_string,
        'features': {}
    }

    features_dict = features()
    for feature in features_dict:
        info = features_dict[feature]
        out['features'][info['module']] = {
            'version': info['version']
        }

    return response.Response(out)


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
