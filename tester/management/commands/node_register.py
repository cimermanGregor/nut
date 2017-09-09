from django.core.management.base import BaseCommand, CommandError
from tester.lib.nut_registrator import NUTRegistrator

# TODO: move into settings.py
API_URL = "http://nut.cime.si:8000"
API_PATH = "api/v1/"
API_TOKEN = "7d069b11a8511424045ec6ac4949367167461b5a"


class Command(BaseCommand):
    help = 'Registers node to central NUT service.'

    def handle(self, *args, **options):

        nr = NUTRegistrator(
            api_url=API_URL, api_path=API_PATH, api_token=API_TOKEN)
        hostname = nr.register_node(include_networks=True)

        self.stdout.write(self.style.SUCCESS(
            "Successfully registered or updated node \"%s\" to NUT" %
            hostname))
