from base64 import b64decode
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import translation
from django.utils.cache import patch_vary_headers


class LocaleMiddleware(object):
    """
    Parse a request and decide what translation object to install in the
    current thread context. This allows pages to be dynamically translated to
    the language the user desires (if the language is available, of course).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = ''
        if request.user and request.user.is_authenticated:
            language = request.user.locale

        if not language:
            language = settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

        response = self.get_response(request)

        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response


class OAuth2TokenMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        oauth = False

        if request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'):
            oauth = True
        elif 'token' in request.POST:
            try:
                token = b64decode(request.POST['token']).decode().split(':')
                if token[0] == request.path:
                    request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + token[1]
                    oauth = True
            except:
                pass

        if oauth and (not hasattr(request, 'user') or request.user.is_anonymous):
            user = authenticate(request=request)
            if user:
                request.user = request._cached_user = user

        response = self.get_response(request)

        patch_vary_headers(response, ('Authorization',))

        return response
