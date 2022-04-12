import os
import sys

from envparse import env

BASE_DIR = env.str('BASE_DIR')

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG')

TESTING = (sys.argv[1:2] == ["test"]) or ("pytest" in sys.modules)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'todo',
    'drf_yasg',
    'crequest',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crequest.middleware.CrequestMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


DEFAULT_DB = 'default'
DATABASES = {
    DEFAULT_DB: {
        'ENGINE': env.str('DB_ENGINE', default="django.db.backends.postgresql"),
        'HOST': env.str('POSTGRES_HOST'),
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'PORT': env.int('POSTGRES_PORT'),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_URL = 'admin/login'

FILE_UPLOAD_PERMISSIONS = 0o644
AUTH_USER_MODEL = 'user.User'

_ = lambda x: x

SITE_HEADER = _('TODO List')
INDEX_TITLE = _('TODO List')
SITE_NAME = _('DORO List')
