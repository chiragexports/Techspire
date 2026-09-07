"""
Django settings for TECHSPIRE Learning LMS project.
"""

from pathlib import Path
import os
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY') or config('SECRET_KEY', default='django-insecure-techspire-learning-key-2026-production-ready-secret-key-indore')
DEBUG = config('DEBUG', default=False, cast=bool) or ('localhost' in os.environ.get('HTTP_HOST', '') or os.environ.get('DEBUG', '').lower() in ['true', '1'])

ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

IS_VERCEL = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))

# ==========================================
# AUTHENTICATION & SESSION PERSISTENCE
# ==========================================
# Use database backed session engine to guarantee robust session persistence
# across cold starts, page refreshes, quiz submissions, and multi-device logins.
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_NAME = 'techspire_sessionid'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 Days persistence
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool) or (IS_VERCEL and not DEBUG)

CSRF_COOKIE_NAME = 'techspire_csrftoken'
CSRF_COOKIE_AGE = 60 * 60 * 24 * 30
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool) or (IS_VERCEL and not DEBUG)

CSRF_TRUSTED_ORIGINS = [
    'https://techspire.vercel.app',
    'https://*.vercel.app',
    'https://*.now.sh',
    'http://127.0.0.1',
    'http://localhost',
]

AUTHENTICATION_BACKENDS = [
    'apps.accounts.backends.PersistentAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]



# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom LMS Apps
    'apps.accounts.apps.AccountsConfig',
    'apps.core.apps.CoreConfig',
    'apps.courses.apps.CoursesConfig',
    'apps.notes.apps.NotesConfig',
    'apps.enrollments.apps.EnrollmentsConfig',
    'apps.quizzes.apps.QuizzesConfig',
    'apps.certificates.apps.CertificatesConfig',
    'apps.dashboard.apps.DashboardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'techspire_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.business_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'techspire_project.wsgi.application'

# Database configuration
# Uses DATABASE_URL (PostgreSQL/Neon/Supabase) if provided, else falls back to SQLite
DATABASE_URL = os.environ.get('DATABASE_URL') or config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # On Vercel serverless, the local filesystem is read-only except /tmp
    is_serverless = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
    if is_serverless:
        import shutil
        tmp_db = Path('/tmp/db.sqlite3')
        possible_sources = [
            BASE_DIR / 'db.sqlite3',
            Path.cwd() / 'db.sqlite3',
            Path('/var/task/db.sqlite3'),
            Path(__file__).resolve().parent.parent / 'db.sqlite3',
        ]
        best_src = None
        best_size = 0
        for src in possible_sources:
            if src.exists() and src.stat().st_size > best_size:
                best_src = src
                best_size = src.stat().st_size

        if best_src:
            dest_size = tmp_db.stat().st_size if tmp_db.exists() else 0
            if dest_size != best_size:
                try:
                    shutil.copy2(best_src, tmp_db)
                except Exception:
                    pass
        db_path = tmp_db
    else:
        db_path = BASE_DIR / 'db.sqlite3'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
        }
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}





# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
WHITENOISE_USE_FINDERS = True




# Media files (User avatars, Course thumbnails, Certificates)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:student_dashboard'
LOGOUT_REDIRECT_URL = 'core:home'

# Email Settings
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='TECHSPIRE Learning <vivekjat301@gmail.com>')

# Business details constants
BUSINESS_INFO = {
    'BRAND_NAME': 'TECHSPIRE Learning',
    'TAGLINE': 'Learn Today, Lead Tomorrow.',
    'BUSINESS_NAME': 'TECHSPIRE',
    'PROPRIETOR_NAME': 'Vivek Jat',
    'BUSINESS_TYPE': 'Proprietorship / Micro Enterprise',
    'LOCATION': 'Indore, Madhya Pradesh, India',
    'ADDRESS': '53/43 Radhaswami Nagar, Nowlakha, Indore, Madhya Pradesh 452001',
    'EMAIL': 'vivekjat301@gmail.com',
    'PHONE': '+91 9713931301',
    'UDYAM': 'UDYAM-MP-23-0283495',
    'GSTIN': '23BEZPJ5728J1ZW',
}
