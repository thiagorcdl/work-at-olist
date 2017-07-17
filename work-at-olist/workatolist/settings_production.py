
from .settings import *
import dj_database_url

# Production code retrieves database information from environment variables
db_from_env = dj_database_url.config(conn_max_age=300)
DATABASES['default'].update(db_from_env)
