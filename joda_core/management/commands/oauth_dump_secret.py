"""Dump OAuth application secret to use in frontend"""

from base64 import b64encode
from django.core.management.base import BaseCommand, CommandError
from oauth2_provider.models import get_application_model

Application = get_application_model()


class Command(BaseCommand):
    """ Management command to dump OAuth application secret in a format to use in frontend
    """

    help = 'Dump OAuth application secret to use in frontend'

    def add_arguments(self, parser):
        parser.add_argument('app_id', type=int, nargs='?', default=1)

    def handle(self, *args, **options):
        try:
            app = Application.objects.get(pk=options['app_id'])
        except Application.DoesNotExist:
            raise CommandError('Application "%s" does not exist' % options['app_id'])

        client_id = app.client_id
        client_secret = app.client_secret

        secret = client_id + ':' + client_secret
        encoded_secret = b64encode(secret.encode('utf-8'))

        self.stdout.write(encoded_secret.decode('utf-8'))
