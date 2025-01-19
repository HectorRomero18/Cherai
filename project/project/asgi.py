"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import sys

path = os.path.expanduser('C:/mi_blog/project')  # Asegúrate de usar la ruta correcta
if path not in sys.path:
    sys.path.insert(0, path)

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.project.settings')

application = get_asgi_application()
