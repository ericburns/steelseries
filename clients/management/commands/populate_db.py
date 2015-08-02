import os
import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from clients.models import Parent, Retailer


class Command(BaseCommand):
    help = 'Populate the Parent and Retailer tables with initial data.'

    def handle(self, *args, **options):
        """Wipe all the data and repopulate."""
        Parent.objects.all().delete()
        Retailer.objects.all().delete()

        parents_filename = os.path.join(settings.BASE_DIR, 'sspythonproj/parents.csv')

        with open(parents_filename, 'rb') as pcsv:
            preader = csv.DictReader(pcsv)

            for row in preader:
                Parent.objects.create(
                    country=row.get('country'),
                    name=row.get('name'),
                    tier=row.get('tier'),
                    start_date=row.get('start_date')
                )

        retailers_filename = os.path.join(settings.BASE_DIR, 'sspythonproj/retailers.csv')

        with open(retailers_filename, 'rb') as rcsv:
            rreader = csv.DictReader(rcsv)

            for row in rreader:
                Retailer.objects.create(
                    name=row.get('name'),
                    parent_name=row.get('parent_name'),
                    country=row.get('country')
                )
