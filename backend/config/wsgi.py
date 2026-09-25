import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django import setup
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

setup()

# Render's current service configuration does not expose a post-deploy hook.
# Run idempotent migrations at startup so a fresh production database is
# initialized before the first API request. Set RUN_MIGRATIONS_ON_STARTUP=false
# if migrations are managed separately in a future deployment pipeline.
if os.getenv("RUN_MIGRATIONS_ON_STARTUP", "true").lower() == "true":
    call_command("migrate", interactive=False, verbosity=0)

application = get_wsgi_application()
