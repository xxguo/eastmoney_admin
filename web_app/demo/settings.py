# Django settings for wictrl project.

import sys
import os.path

import imp
imp.reload(sys)
sys.setdefaultencoding('utf-8')

from django.utils.translation import ugettext_lazy as _


PROJECT_ROOT = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), os.pardir)
# PROJECT_ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CHARSET = 'utf-8'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60*25

# DEBUG = True
DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'account_admin',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'password_123_Admin',                  # Not used with sqlite3.
        'HOST': '47.96.67.154',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        'CHARSET': 'utf8',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    },
    'cms': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crawl_data',
        'USER': 'root',
        'PASSWORD': 'password_123_Admin',
        'HOST': '47.96.67.154',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'CHARSET': 'utf8'
    },
}

DATABASE_ROUTERS = ['demo.db_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    'cms': 'cms',
    'admin': 'default',
    'default':  'default',
    'symbol_cons':  'cms',
    'statistics':  'cms',
    # 'symbol_cons': 'symbol_cons',
    # 'xysl_dwm': 'xysl_dwm',
    # 'xysl_ods': 'xysl_ods'
}

IMPORT_EXPORT_USE_TRANSACTIONS = False
# IMPORT_EXPORT_SKIP_ADMIN_LOG = True

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-Hans'

LANGUAGES = (
    # ('en', _('English')),
    ('zh-hans', _('Chinese')),
)

SITE_ID = 1

DATETIME_FORMAT = 'Y-m-d H:i:s'

DATE_FORMAT = 'Y-m-d'
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
if DEBUG:
    STATIC_ROOT = 'static/'
else:
    STATIC_ROOT = '/root/project/eastmoney/web_app/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5=!nss_+^nvyyc_j(tdcf!7(_una*3gtw+_8v5jaa=)j0g^d_2'

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'demo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'demo.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT,"templates"),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'xadmin',
    'crispy_forms',
    'reversion',

    'import_export',

    'app',
    'cms',
    'symbol_cons',
    'statistics'
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # }
    }
}
