import os
from pathlib import Path
from decouple import config
from datetime import timedelta

# ──────────────────────────────────────────────────────────────────────────────
# Base directory
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ──────────────────────────────────────────────────────────────────────────────
# Security & Hosts
# ──────────────────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# ──────────────────────────────────────────────────────────────────────────────
# Tenancy (django-tenants)
# ──────────────────────────────────────────────────────────────────────────────
TENANT_MODEL = 'apps.tenants.Tenant'
TENANT_DOMAIN_MODEL = 'apps.tenants.Domain'
DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']

# ──────────────────────────────────────────────────────────────────────────────
# Application definition
# ──────────────────────────────────────────────────────────────────────────────
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'django_tenants',               # must come before any django apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'celery',
    'django_celery_beat',
    'django_celery_results',
    'tenant_users',                 # per-tenant user model
]

# Shared apps live in the public (shared) schema
SHARED_APPS = [
    *DJANGO_APPS,
    'apps.core',
    'apps.accounts',
    'apps.module_manager',
    'apps.tenants',
]

# Apps that live in each tenant’s schema
TENANT_APPS = [
    *THIRD_PARTY_APPS,
] + [
    f'apps.hr_modules.{mod}'
    for mod in config(
        'ENABLED_MODULES',
        default='employees,time_attendance,leave_management,payroll,performance,recruitment,benefits,learning'
    ).split(',')
]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.TimezoneMiddleware',
    'apps.core.middleware.AuditMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# ──────────────────────────────────────────────────────────────────────────────
# Database (PostgreSQL for all schemas)
# ──────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     config('DB_NAME'),
        'USER':     config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST':     config('DB_HOST'),
        'PORT':     config('DB_PORT', default='5432'),
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# Auth & Users
# ──────────────────────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'tenant_users.TenantUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'apps.accounts.validators.CustomPasswordValidator'},
]

# ──────────────────────────────────────────────────────────────────────────────
# Internationalization
# ──────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────────────────────
# Static & Media
# ──────────────────────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────────────────────────────────────────────────────
# Sites framework
# ──────────────────────────────────────────────────────────────────────────────
SITE_ID = 1

# ──────────────────────────────────────────────────────────────────────────────
# REST Framework
# ──────────────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# ──────────────────────────────────────────────────────────────────────────────
# Simple JWT
# ──────────────────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':      timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME':     timedelta(days=7),
    'ROTATE_REFRESH_TOKENS':      True,
    'BLACKLIST_AFTER_ROTATION':   True,
    'UPDATE_LAST_LOGIN':          True,
    'ALGORITHM':                  'HS256',
    'SIGNING_KEY':                SECRET_KEY,
    'AUTH_HEADER_TYPES':          ('Bearer',),
    'AUTH_HEADER_NAME':           'HTTP_AUTHORIZATION',
    'USER_ID_FIELD':              'id',
    'USER_ID_CLAIM':              'user_id',
    'AUTH_TOKEN_CLASSES':         ('rest_framework_simplejwt.tokens.AccessToken',),
    'SLIDING_TOKEN_LIFETIME':     timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# ──────────────────────────────────────────────────────────────────────────────
# Spectacular / OpenAPI
# ──────────────────────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    'TITLE':                'HRMIS API',
    'DESCRIPTION':          'Human Resource Management Information System API',
    'VERSION':              '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX':   '/api/v1/',
    'COMPONENT_SPLIT_REQUEST': True,
}

# ──────────────────────────────────────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
CORS_ALLOW_CREDENTIALS = True

# ──────────────────────────────────────────────────────────────────────────────
# Celery & Redis
# ──────────────────────────────────────────────────────────────────────────────
REDIS_URL = config('REDIS_URL')  # your online Redis URL
CELERY_BROKER_URL    = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE       = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# ──────────────────────────────────────────────────────────────────────────────
# Cache
# ──────────────────────────────────────────────────────────────────────────────
CACHES = {
    'default': {
        'BACKEND':  'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS':  {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# Sessions
# ──────────────────────────────────────────────────────────────────────────────
SESSION_ENGINE      = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE  = 3600
SESSION_COOKIE_SECURE   = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# ──────────────────────────────────────────────────────────────────────────────
# Email Configuration
# ──────────────────────────────────────────────────────────────────────────────
EMAIL_BACKEND    = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST       = config('EMAIL_HOST', default='localhost')
EMAIL_PORT       = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS    = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER  = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL   = config('DEFAULT_FROM_EMAIL', default='noreply@hrmis.com')

# ──────────────────────────────────────────────────────────────────────────────
# File upload limits
# ──────────────────────────────────────────────────────────────────────────────
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_PERMISSIONS   = 0o644

# ──────────────────────────────────────────────────────────────────────────────
# Security headers
# ──────────────────────────────────────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER   = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS             = 'DENY'

# ──────────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────────
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
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {'handlers': ['file', 'console'], 'level': 'INFO', 'propagate': False},
        'apps':   {'handlers': ['file', 'console'], 'level': 'INFO', 'propagate': False},
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# API Version & HRMIS custom settings
# ──────────────────────────────────────────────────────────────────────────────
API_VERSION = 'v1'

HRMIS_SETTINGS = {
    'COMPANY_NAME':           config('COMPANY_NAME', default='HRMIS System'),
    'SUPPORT_EMAIL':          config('SUPPORT_EMAIL', default='support@hrmis.com'),
    'MAX_EMPLOYEES_PER_TENANT': config('MAX_EMPLOYEES_PER_TENANT', default=1000, cast=int),
    'DEFAULT_PAGINATION_SIZE':   20,
    'MAX_PAGINATION_SIZE':       100,
    'PASSWORD_RESET_TIMEOUT':    3600,
    'TENANT_SUBDOMAIN_VALIDATION': True,
    'MULTI_TENANT_MODE':          True,
    'DEFAULT_TIMEZONE':           'UTC',
    'SUPPORTED_LANGUAGES':        ['en', 'fr', 'es'],
    'FILE_TYPES_ALLOWED': [
        'pdf', 'doc', 'docx', 'xls', 'xlsx',
        'jpg', 'jpeg', 'png', 'gif'
    ],
    'MAX_FILE_SIZE': 5 * 1024 * 1024,
}

MODULE_SETTINGS = {
    'ENABLED_MODULES': [
        'employees',
        'time_attendance',
        'leave_management',
        'payroll',
        'performance',
        'recruitment',
        'benefits',
        'learning',
    ],
    'MODULE_PERMISSIONS': {
        'employees':      ['view', 'add', 'change', 'delete'],
        'payroll':        ['view', 'add', 'change', 'delete', 'process'],
        'time_attendance':['view', 'add', 'change', 'approve'],
        'leave_management':['view', 'add', 'change', 'approve'],
        'performance':    ['view', 'add', 'change', 'evaluate'],
        'recruitment':    ['view', 'add', 'change', 'hire'],
        'benefits':       ['view', 'add', 'change', 'enroll'],
        'learning':       ['view', 'add', 'change', 'enroll'],
    },
}

# Ensure logs directory exists
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
