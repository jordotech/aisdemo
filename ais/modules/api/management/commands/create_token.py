from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = "Creates an API auth token assigned to the given username. \n " \
           "Usage: ./manage.py create_token foo@domain.com --refresh"


    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('email', nargs='+', type=str)

        # Named (optional) arguments
        parser.add_argument('--refresh',
                            action='store_true',
                            dest='refresh',
                            default=False,
                            help='Force deletion of existing token before creation')

    def handle(self, **options):
        email = options.get('email')[0]
        refresh = options['refresh']

        try:
            user = User.objects.get(email__iexact=email)
            if refresh:
                Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            if token:
                self.stdout.write(self.style.SUCCESS('Token created: %s' % token.key))
        except User.DoesNotExist:
            raise CommandError('User with email (%s) does not exist.' % email)