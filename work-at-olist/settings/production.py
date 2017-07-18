"""
    Settings file for production code
"""
import dj_database_url

from .base import *

DEBUG = False

# Production code retrieves database information from environment variables
db_from_env = dj_database_url.config(conn_max_age=300)
DATABASES['default'].update(db_from_env)

# Heroku domain clearance
ALLOWED_HOSTS.extend([".herokuapp.com", ])