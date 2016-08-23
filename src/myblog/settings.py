import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ylfe!ogn2og%iqpq7ln0$_i+vvv^%hv#9=d@zh*62e4$b28^&s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    'crispy_forms',
    'markdown_deux',
    'pagedown',

    # local apps
    'comments',
    'posts',
    'ckeditor',
    'ckeditor_uploader',

]

MARKDOWN_DEUX_STYLES = {
"default": {
"extras": {
"code-friendly": None,
},
"safe_mode": False,
},
}


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"
CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL = "/login/"
ROOT_URLCONF = 'myblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

CKEDITOR_CONFIGS = {
'default': {
'skin': 'moono',
#'skin': 'office2013',
'toolbar_Basic': [
['Source', '-', 'Bold', 'Italic']
],
'toolbar_YouCustomToolbarConfig': [
{'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
{'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
{'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
{'name': 'forms',
'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
'HiddenField']},
'/',
{'name': 'basicstyles',
'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
{'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                                'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl','Language']},
{'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
{'name': 'insert','items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
{'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
{'name': 'colors', 'items': ['TextColor', 'BGColor']},
{'name': 'tools', 'items': ['Maximize', 'ShowBlocks','Preview']},
{'name': 'about', 'items': ['About']},
#'/', # put this to force next toolbar on new line
#{'name': 'youcustomtools',
# 'items': [
#            # put the name of your editor.ui.addButton here
#            'Preview',
#            'Maximize',
#          ]
#},
],
'toolbar': 'YouCustomToolbarConfig',
# put selected toolbar config here
# 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
# 'height': 291,
# 'width': '100%',
# 'filebrowserWindowHeight': 725,
# 'filebrowserWindowWidth': 940,
# 'toolbarCanCollapse': True,
# 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML'
'tabSpaces': 4,
'extraPlugins': ','.join(
[
# you extra plugins here
'div',
'autolink',
'autoembed',
'embedsemantic',
'autogrow',
# 'devtools',
'widget',
'lineutils',
'clipboard',
'dialog',
'dialogui',
'elementspath'
]),
}
}
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    )
#STATIC_ROOT = os.path.join(os.path.dirname(os.path.join(BASE_DIR, "static")), "static")
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
#Media files configuration
MEDIA_URL = "/media/"
#MEDIA_ROOT = os.path.join(os.path.dirname(os.path.join(BASE_DIR, "static")), "static/media")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static/media")
#Email configuration
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'contact.xchangeidea@gmail.com'
#EMAIL_HOST_PASSWORD = 'pass@word'
#DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'e@mail.xchangeidea.net'
EMAIL_HOST_PASSWORD = 'xchangeidea'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
