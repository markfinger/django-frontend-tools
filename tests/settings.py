import os

BASE_DIR = os.path.dirname(__file__)


# DJANGO
# ======

SECRET_KEY = '_'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = ()

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static_root'))

STATIC_URL = '/static/'


# DJANGO NODE
# ===========

INSTALLED_APPS += (
    'django_node',
)

DJANGO_NODE = {
    'SERVICES': (
        'django_frontend_tools.services',
    )
}


# DJANGO COMPRESSOR
# =================

INSTALLED_APPS += (
    'compressor',
)

COMPRESS_ENABLED = True

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = [
    'django_frontend_tools.filters.CompressCSSFilter',
]

COMPRESS_JS_FILTERS = [
    'django_frontend_tools.filters.CompressJSFilter',
]


# DJANGO FRONTEND TOOLS
# =====================

INSTALLED_APPS += (
    'django_frontend_tools',
)


# TESTS
# =====

STATICFILES_DIRS += (
    os.path.join(BASE_DIR, 'test_static'),
)

INSTALLED_APPS += (
    'tests.test_app',
)