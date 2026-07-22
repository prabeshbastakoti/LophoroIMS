"""Entry point for cPanel's "Setup Python App" (Phusion Passenger).

Passenger imports this file and looks for a module-level ``application``.
Point the app's "Application startup file" at ``passenger_wsgi.py`` in cPanel.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lophoroims.settings')

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
