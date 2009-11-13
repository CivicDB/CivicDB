import os

DATA_UPLOAD_PATH='/tmp'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
GRAPHVIZ_DOT_CMD = "C:/Program Files/Graphviz2.22/bin"

STATIC_DATA = os.path.join(os.path.dirname(__file__), 'static/')
ADMINS = (
    ('Admin1', 'josh@umbrellaconsulting.com'),
)
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

MANAGERS = ADMINS
ACCOUNT_ACTIVATION_DAYS = 5
DEFAULT_FROM_EMAIL= 'civicdb@umbrellaconsulting.com'
EMAIL_MANAGERS = False

EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='django_emails@umbrellaconsulting.com'
EMAIL_HOST_PASSWORD='2S7538'
EMAIL_PORT= 587
EMAIL_USE_TLS = True

EMAIL_DEBUG = True

if EMAIL_DEBUG:
  DEBUG_EMAIL_ADDR = 'josh@umbrellaconsulting.com'
  DEFAULT_FROM_EMAIL = DEBUG_EMAIL_ADDR
  MANAGERS = ('Debug Manager','%s' % DEBUG_EMAIL_ADDR)

CACHE_BACKEND = 'file:///tmp/civicdb_cache'

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'civicdb'             # Or path to database file if using sqlite3.
DATABASE_USER = 'civi'             # Not used with sqlite3.
DATABASE_PASSWORD = 'tk3'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2l!b-w*l869krj2r4xte#-st^&8uh!k=bdvq5t!j5djr63-xug'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfViewMiddleware',
    'django.contrib.csrf.middleware.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'civicdb.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.databrowse',
    'django.contrib.gis',
    'django.contrib.humanize',
    'django.contrib.webdesign',
    'registration',
    'profiles',
    'metadata',
)

try:
    from local_settings import *
except ImportError, exp:
    pass
