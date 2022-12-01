"""
Django settings for lfjennings project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-lxa(o7e6+i6_gbpt3g+l2^^p0lc1!$jw%+zpuxt8e-2^y=xx(4'

# SECURITY WARNING: don't run with debug turned on in production
DEBUG = True

ALLOWED_HOSTS = ['*','marcowolff.me']

INSTALLED_APPS = [
    'login_app',
    'main',
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lfjennings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            ],
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

WSGI_APPLICATION = 'lfjennings.wsgi.application'
load_dotenv()


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
#aws user admin and pass Charlie23##
 

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         'NAME': "wolffdb",
#         'USER': "admin",
#         'PASSWORD': "Charlie23##$$%%",
#         'HOST': "wolffdb.cvopqdkkwgwq.us-east-1.rds.amazonaws.com",
#         'PORT': "3306",
#     	'OPTIONS': {
#             'sql_mode': 'traditional',
#         }
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
    	'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS':{
            'min_length':4,
        }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_TZ = True

 
LOGIN_REDIRECT_URL = 'login'
LOGOUT_REDIRECT_URL = 'logout'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/img/'

USE_S3 = os.getenv('USE_S3') == 'TRUE'
AWS_ACCESS_KEY_ID = 'AKIAURUAQBNXSNYUCBUW' 
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'lfj'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)



CSRF_TRUSTED_ORIGINS = ['https://marcowolff.me/*','https://keybyme.net','http://keybyme.net']
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



#smtp configuration
#EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'flooringsvc@gmail.com'
EMAIL_HOST_PASSWORD = 'ayflfnxxhkptlvwz' 
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False
