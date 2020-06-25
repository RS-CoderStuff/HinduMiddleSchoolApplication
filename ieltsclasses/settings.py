"""
Django settings for ieltsclasses project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'go1(-er^l&1r$g^7)pgv)g_r9ugc%uwq6(@mi+!&0cnn3sau2#'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['*','192.168.1.10']

WEB_SITE_URL = 'http://ec2-18-218-21-56.us-east-2.compute.amazonaws.com/'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'ieltsapp',
    'apiapp',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dal',
    'dal_select2',
    "fcm_django",

]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.auth.backends.ModelBackend',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ieltsapp.middleware.OneSessionPerUserMiddleware',


]

ROOT_URLCONF = 'ieltsclasses.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'ieltsapp.staticencoder'
            ],
        },
    },
]

WSGI_APPLICATION = 'ieltsclasses.wsgi.application'



#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hindu',
        'USER': 'hinduApp',
        'PASSWORD': 'app@hindu',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# DATABASES = {
#     'default':{
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'tec',
#         'USER':'tec',
#         'PASSWORD':'asdfghjkl',
#         'PORT': '3306',
#         'HOST':'tec.cpsgxbhqao49.us-east-2.rds.amazonaws.com',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
            'min_length': 8,
        }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


AUTHENTICATION_BACKENDS = (


    # 'phone_login.backends.phone_backend.PhoneBackend', #login with phone
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.AllowAllUsersModelBackend'

)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
   'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),

}



# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'



USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

####################################
##  CKEDITOR CONFIGURATION ##
####################################
AUTH_USER_MODEL = 'ieltsapp.User'

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_ALLOW_NONIMAGE_FILES = False

# config ckeditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': (
            ['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker', 'Scayt'],
            ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
        ),
    }
}


SITE_ID = 1


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED =True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT =587 #465# Gmail SMTP port for TLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'info@teconline.in'
EMAIL_HOST_PASSWORD = 'Tajinder@2003'
DEFAULT_FROM_EMAIL = 'info@teconline.in'


LOGIN_URL ='/sign-in'



STATIC_URL = '/static/'
# STATIC_ROOT =''
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Add these new lines
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
#

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
CKEDITOR_UPLOAD_PATH = 'uploads/'



FCM_DJANGO_SETTINGS = {

        "APP_VERBOSE_NAME": "[string for AppConfig's verbose_name]",
         # default: _('FCM Django')
        "FCM_SERVER_KEY": "AAAABmInxvA:APA91bHg6X6JwgX6hk4qa5W6Bnu0TwYmFaUUjIvPMYjOHLMtYH0XCd3OC1mG6IGMVVICcMlXPmq9KiIr0qa8Z6gD-kKnRPVZBkgmRCMQtIV50sJ49OGPNGDSY0kvjSumKGp23_ra4CHO",
         # true if you want to have only one active device per registered user at a time
         # default: False
        "ONE_DEVICE_PER_USER": True,
         # devices to which notifications cannot be sent,
         # are deleted upon receiving error response from FCM
         # default: False
        "DELETE_INACTIVE_DEVICES": False,
}


