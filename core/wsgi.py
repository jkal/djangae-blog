"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

from core.boot import fix_path
fix_path()

import os
from django.core.wsgi import get_wsgi_application
from djangae.wsgi import DjangaeApplication
from djangae.utils import on_production

settings = "core.settings_live" if on_production() else "core.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

application = DjangaeApplication(get_wsgi_application())
