"""
WSGI config for restaurant_managment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_managment.settings')

application = get_wsgi_application()


