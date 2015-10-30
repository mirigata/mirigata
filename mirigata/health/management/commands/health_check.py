from django.core.management import BaseCommand
import sys
from health import views


class Command(BaseCommand):
    help = 'Run all basic health checks'

    def handle(self, *args, **options):
        response = views.health(None)
        if response.status_code != 200:
            self.stderr.write("Health check failed")
            sys.exit(-1)

        else:
            self.stdout.write("Health check succeeded")
