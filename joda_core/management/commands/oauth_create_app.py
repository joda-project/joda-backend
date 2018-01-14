"""Create (inital) OAuth application"""

from django.core.management.base import BaseCommand, CommandError
from oauth2_provider.models import get_application_model

Application = get_application_model()


class Command(BaseCommand):
    """ Management command to create (inital) OAuth application
        If application already exists, use --force to duplicate.
    """

    help = 'Create (initial) OAuth application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            help='Force adding a new application even if one already exists.',
        )

    def handle(self, *args, **options):
        # Check for existence of applications
        if Application.objects.count() and not options['force']:
            raise CommandError('The initial OAuth application already exists.')

        app = Application.objects.create(
            name='Joda Frontend',
            skip_authorization=True,
            client_type='confidential',
            authorization_grant_type='password'
        )
        app.save()

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created application "%s" with id "%d"' % (app.name, app.id))
        )
