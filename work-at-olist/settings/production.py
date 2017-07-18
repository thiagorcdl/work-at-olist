"""
    Settings file for production code
"""
import dj_database_url

from .base import *

DEBUG = False

# Production code retrieves database information from environment variables
db_from_env = dj_database_url.config(conn_max_age=300)
DATABASES['default'].update(db_from_env)

# Production code retrieves secret key from environment variables
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    raise ValueError(u'You must define a SECRET_KEY environment  variable '
                     u'for production.')

# Heroku domain clearance
ALLOWED_HOSTS.extend([".herokuapp.com", ])

# Deployment Security Definitions
SECURE_CONTENT_TYPE_NOSNIFF = True  # helps browser identifying content types
SECURE_BROWSER_XSS_FILTER = True  # helps prevent XSS attacks
SESSION_COOKIE_SECURE = True  # makes session hijacking more difficult
CSRF_COOKIE_SECURE = True  # makes form sniffing more difficult
X_FRAME_OPTIONS = 'DENY'  # prevents loading from within an iframe
