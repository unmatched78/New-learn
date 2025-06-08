# config/settings/development.py
"""
Development settings for HRMIS project.
This file contains settings specific to the development environment.
"""

import os
import sys
from datetime import timedelta
from .base import *  # noqa: F401,E261,E501

# ──────────────────────────────────────────────────────────────────────────────
# General
# ──────────────────────────────────────────────────────────────────────────────
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '.ngrok.io', '.localhost.run']
ENVIRONMENT = 'development'

# ──────────────────────────────────────────────────────────────────────────────
# Database
# ──────────────────────────────────────────────────────────────────────────────
# Use SQLite for quick development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# In-memory DB when running tests
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    # Disable migrations for faster tests
    class DisableMigrations:
        def __contains__(self, item):
            return True
        def __getitem__(self, item):
            return None
    MIGRATION_MODULES = DisableMigrations()

# ──────────────────────────────────────────────────────────────────────────────
# Caching & Celery (use your online Redis)
# ──────────────────────────────────────────────────────────────────────────────
REDIS_URL = os.getenv('REDIS_URL')  # must be set in your environment

# Cache
CACHES = {
    'default': {
        'BACKEND':  'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS':  {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}
SESSION_ENGINE      = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Celery
CELERY_BROKER_URL         = REDIS_URL
CELERY_RESULT_BACKEND     = REDIS_URL
CELERY_ACCEPT_CONTENT     = ['json']
CELERY_TASK_SERIALIZER    = 'json'
CELERY_RESULT_SERIALIZER  = 'json'
CELERY_TIMEZONE           = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER  = True   # run tasks locally
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_TASK_RESULT_EXPIRES = 60 * 60  # 1 hour

# ──────────────────────────────────────────────────────────────────────────────
# Tenant auto-creation
# ──────────────────────────────────────────────────────────────────────────────
TENANT_SETTINGS = {
    'AUTO_CREATE_SCHEMA': True,
    'AUTO_DROP_SCHEMA':   True,
    'DEFAULT_TENANT_DOMAIN': 'localhost:8000',
}

# ──────────────────────────────────────────────────────────────────────────────
# Static & Media
# ──────────────────────────────────────────────────────────────────────────────
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_ROOT         = BASE_DIR / 'media'

# ──────────────────────────────────────────────────────────────────────────────
# Email
# ──────────────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST    = 'localhost'
EMAIL_PORT    = 1025  # e.g. MailHog
EMAIL_USE_TLS = False
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# ──────────────────────────────────────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

# ──────────────────────────────────────────────────────────────────────────────
# Security adjustments for dev
# ──────────────────────────────────────────────────────────────────────────────
SECURE_SSL_REDIRECT          = False
SECURE_HSTS_SECONDS          = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD          = False
SECURE_CONTENT_TYPE_NOSNIFF  = False
SECURE_BROWSER_XSS_FILTER    = False
SESSION_COOKIE_SECURE        = False
CSRF_COOKIE_SECURE           = False

# ──────────────────────────────────────────────────────────────────────────────
# Installed Apps & Middleware
# ──────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1', 'localhost']

# ──────────────────────────────────────────────────────────────────────────────
# Debug Toolbar
# ──────────────────────────────────────────────────────────────────────────────
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# ──────────────────────────────────────────────────────────────────────────────
# REST Framework (Browsable API)
# ──────────────────────────────────────────────────────────────────────────────
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
    'rest_framework.renderers.BrowsableAPIRenderer',
]

# ──────────────────────────────────────────────────────────────────────────────
# Simple JWT (shorter tokens in dev)
# ──────────────────────────────────────────────────────────────────────────────
SIMPLE_JWT.update({
    'ACCESS_TOKEN_LIFETIME':  timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
})

# ──────────────────────────────────────────────────────────────────────────────
# Spectacular (enable UI)
# ──────────────────────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS.update({
    'SERVE_INCLUDE_SCHEMA': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
})

# ──────────────────────────────────────────────────────────────────────────────
# File uploads & Custom HRMIS overrides
# ──────────────────────────────────────────────────────────────────────────────
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

HRMIS_SETTINGS.update({
    'MAX_EMPLOYEES_PER_TENANT':      10000,
    'TENANT_SUBDOMAIN_VALIDATION':   False,
    'MAX_FILE_SIZE':                 50 * 1024 * 1024,
})

# ──────────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────────
LOGGING['handlers']['file']['filename'] = BASE_DIR / 'logs' / 'development.log'
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django.db.backends']['level'] = 'DEBUG'
LOGGING['loggers']['apps']['level'] = 'DEBUG'
LOGGING['loggers']['celery']['level'] = 'DEBUG'

# ──────────────────────────────────────────────────────────────────────────────
# Shell Plus
# ──────────────────────────────────────────────────────────────────────────────
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000

# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────
FIXTURE_DIRS = [BASE_DIR / 'fixtures']

# ──────────────────────────────────────────────────────────────────────────────
# Final confirmation
# ──────────────────────────────────────────────────────────────────────────────
print("🚀 Development settings loaded successfully!")
print(f"📁 BASE_DIR: {BASE_DIR}")
print(f"🗄️  Database: {DATABASES['default']['NAME']}")
print(f"📧 Email Backend: {EMAIL_BACKEND}")
print(f"🌐 CORS Allowed Origins: {CORS_ALLOWED_ORIGINS}")
print(f"🔧 Debug Mode: {DEBUG}")
