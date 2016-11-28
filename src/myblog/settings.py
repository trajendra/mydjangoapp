import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ylfe!ogn2og%iqpq7ln0$_i+vvv^%hv#9=d@zh*62e4$b28^&s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # local apps
    'comments',
    'posts',
    'ckeditor',
    'ckeditor_uploader',
    'profiles',

    # third party
    'crispy_forms',
    'markdown_deux',
    'pagedown',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.twitter',

]
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 15
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
LOGIN_REDIRECT_URL = "/"


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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        #'ENGINE': 'sql_server.pyodbc',
        #'NAME': 'SQLAzureDB',
        #'USER': 'trajendra@myserver',
        #'PASSWORD': '04june@1985',
        #'HOST': 'sqldbazure.database.windows.net',
        #'PORT': '',

        #'OPTIONS': {
        #    'driver': 'ODBC Driver 13 for SQL Server',
        #},
        #'NAME': 'my_database',
        #'ENGINE': 'sqlserver_ado',
        #'HOST': 'dbserver\\ss2008',
        #'USER': '',
        #'PASSWORD': '',
    }
}

# set this to False if you want to turn off pyodbc's connection pooling
#DATABASE_CONNECTION_POOLING = False

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

    'awesome_ckeditor': {'toolbar':'Full',
        'height': 100,
        'width': '100%',
        'toolbarCanCollapse': True,

                         },

    'default': {
        'skin': 'moono',

        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
         ],

        'toolbar_YouCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source' , '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            #{'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},

            #{'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            #{'name': 'forms','items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton','HiddenField']},
            #'/',

            {'name': 'insert','items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                                            'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl','Language']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks', 'Preview']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},

            #{'name': 'about', 'items': ['About']},
         ],

        'toolbar': 'YouCustomToolbarConfig',

         #put selected toolbar config here
         'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],

         'height': 100,
         'width': '100%',
         'filebrowserWindowHeight': 725,
         'filebrowserWindowWidth': 940,
         'toolbarCanCollapse': True,
         #'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML'
         'tabSpaces': 4,

        #'extraPlugins': ','.join(
        #[
        # you extra plugins here
        #'div',
        #'autolink',
        #'autoembed',
        #'embedsemantic',
        #'autogrow',
        # 'devtools',
        #'widget',
        #'lineutils',
        #'clipboard',
        #'dialog',
        #'dialogui',
        #'elementspath'
        #]),

        }
}
# Internationalization

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

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_#PORT = 587
#EMAIL_HOST_USER = 'xyz@gmail.com'
#EMAIL_HOST_PASSWORD = 'pass@word'
#DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.mailgun.org'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'xyz@gmail.com'
#EMAIL_HOST_PASSWORD = 'pass@word'
#DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SOCIALACCOUNT_PROVIDERS = \
    { 'google':
        { 'SCOPE': ['profile', 'email'],
          'AUTH_PARAMS': { 'access_type': 'online' } },

    'linkedin':
      {'SCOPE': ['r_emailaddress'],
       'PROFILE_FIELDS': ['id',
                         'first-name',
                         'last-name',
                         'email-address',
                         'picture-url',
                         'public-profile-url']},

      'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US',
        'VERIFIED_EMAIL': True,
        'VERSION': 'v2.4'},

        'openid':
        { 'SERVERS':
            [dict(id='yahoo',
                  name='Yahoo',
                  openid_url='http://me.yahoo.com'),
             dict(id='hyves',
                  name='Hyves',
                  openid_url='http://hyves.nl'),
             dict(id='google',
                  name='Google',
                  openid_url='https://www.google.com/accounts/o8/id')]}

          }

