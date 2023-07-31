"""
WSGI config for tourney project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application
sys.path.append("/home/fenyan.helioho.st/httpdocs/tourney")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourney.settings')

application = get_wsgi_application()
