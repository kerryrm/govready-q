import sys
import os.path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, models
from django.db.utils import OperationalError
from django.conf import settings

from guidedmodules.models import AppSource, Module
from siteapp.models import User, Organization, Portfolio
from django.contrib.auth.management.commands import createsuperuser
from siteapp.models import User, Project, Organization, Portfolio, Folder
from controls.models import System, Element, ElementControl

import fs, fs.errors


class Command(BaseCommand):
    help = 'Load GovReady-Q Sample Project'

    def add_arguments(self, parser):
        # parser.add_argument('forever', nargs='?', type=bool)
        parser.add_argument('--non-interactive', action='store_true')

    def handle(self, *args, **options):
        # Return a simple value
        print("Running load_govready_ssp")

        # Check if projects already exist
        project_count = len(Project.objects.all())
        if project_count > 1:
            print("Confirmed GovReady-Q currently has projects.")
            # We're done
        else:
            # No projects exist, so load default GovReady Project
            print("Adding GovReady-Q Project and SSP.")

            # Set defaults for testing
            self.org = Organization.objects.first()
            print(self.org.slug)
            # hardcode user for dev
            user = User.objects.get(username="admin")

            from loadtesting.web import WebClient
            client = WebClient("admin", "main")

            portfolio = Portfolio.objects.first()
            print("Adding project to portfolio: {} (#{})".format(portfolio.title, portfolio.id))
            client.post("/store/govready-q-files-startpack/lightweight-ato?portfolio={}".format(portfolio.id), {"organization":self.org.slug})
            print(client.response.url)

            print("Project created")