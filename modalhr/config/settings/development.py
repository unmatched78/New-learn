# config/settings/development.py
"""
Development settings for HRMIS project.
This file contains settings specific to development environment.
"""

from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Development specific allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '.ngrok.io', '.localhost.run']

# # Development Database Configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default='hrmis_dev'),
#         'USER': config('DB_USER', default='postgres'),
#         'PASSWORD': config('DB_PASSWORD', default='postgres'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#         'OPTIONS': {
#             'charset': 'utf8',
#         },
#         'CONN_MAX_AGE': 0,  # Don't persist connections in development
#     }
# }

# Alternative SQLite database for quick development
# Uncomment the following to use SQLite instead of PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Development Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development Static Files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Development Media Files
MEDIA_ROOT = BASE_DIR / 'media'

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True

# Development Security Settings
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Development Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'hrmis-dev-cache',
    }
}

# Alternative Redis cache for development (if you have Redis running)
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://localhost:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

# Development Celery Configuration
CELERY_TASK_ALWAYS_EAGER = True  # Execute tasks synchronously in development
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Development specific installed apps
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

# Development specific middleware
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Debug Toolbar Configuration
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# Development REST Framework settings
REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Add browsable API in dev
    ],
})

# Development JWT Configuration (shorter lifetimes for testing)
SIMPLE_JWT.update({
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
})

# Development Spectacular Settings
SPECTACULAR_SETTINGS.update({
    'SERVE_INCLUDE_SCHEMA': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
})

# Development File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB for development
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB for development

# Development Custom HRMIS Settings
HRMIS_SETTINGS.update({
    'MAX_EMPLOYEES_PER_TENANT': 10000,  # Higher limit for development
    'TENANT_SUBDOMAIN_VALIDATION': False,  # Disable for easier development
    'MAX_FILE_SIZE': 50 * 1024 * 1024,  # 50MB for development
})

# Development Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '{log_color}{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'development.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Show SQL queries in development
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Development shell plus configuration
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000

# Development fixture directories
FIXTURE_DIRS = [
    BASE_DIR / 'fixtures',
]

# Development email configuration for testing
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025  # For local SMTP server like MailHog
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Development testing database
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }

# Development environment variables
ENVIRONMENT = 'development'

# Disable migrations for faster testing
if 'test' in sys.argv:
    class DisableMigrations:
        def __contains__(self, item):
            return True
        
        def __getitem__(self, item):
            return None
    
    MIGRATION_MODULES = DisableMigrations()

# Development tenant settings
TENANT_SETTINGS = {
    'AUTO_CREATE_SCHEMA': True,
    'AUTO_DROP_SCHEMA': True,
    'DEFAULT_TENANT_DOMAIN': 'localhost:8000',
}

# Development password validation (less strict)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,  # Shorter for development
        }
    },
]

print("🚀 Development settings loaded successfully!")
print(f"📁 BASE_DIR: {BASE_DIR}")
print(f"🗄️  Database: {DATABASES['default']['NAME']}")
print(f"📧 Email Backend: {EMAIL_BACKEND}")
print(f"🌐 CORS Allowed Origins: {CORS_ALLOWED_ORIGINS}")
print(f"🔧 Debug Mode: {DEBUG}")