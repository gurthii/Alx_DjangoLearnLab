import os
import sys

# Add your project directory to the path
path = '/home/yourusername/social_media_api/' # <-- Update this path!
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'social_media_api.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()