# coding=utf-8
import os, sys
import random

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))



def load_settings(settings, debug=True, **kwargs):
    settings.update(
        {
            'TEMPLATE_LOADERS': (
                (
                    'django.template.loaders.cached.Loader',
                    (
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    )
                ),
            ),

            'DEBUG': debug,
            'TEMPLATE_DEBUG': debug,
            'TEST': False,
            'CHINA_CACHE_DOWNLOAD_URL': "http://dl.g.libai.com/",
            'PROJECT_ROOT': PROJECT_ROOT,
            'ANONYMOUS_USER_ID': -1,

            'TEMPLATE_DIRS': (
                os.path.join(PROJECT_ROOT, "templates"),
                os.path.join(PROJECT_ROOT, "content/templates"),
                os.path.join(PROJECT_ROOT, "user/templates"),
            ),

            'ROOT_URLCONF': 'app.urls',
            'STATICFILES_FINDERS': [
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            ],
            'STATICFILES_DIRS': (
                os.path.join(PROJECT_ROOT, 'statics'),
            ),
            "STATIC_ROOT": os.path.join(PROJECT_ROOT, 'statics'),
            'TEMPLATE_CONTEXT_PROCESSORS': (
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                'django.core.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                "django.contrib.auth.context_processors.auth",),

            'MIDDLEWARE_CLASSES': [
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                # 'app.permission.middleware.PermMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.transaction.TransactionMiddleware',
                'app.middleware.profile_middleware.ProfileMiddleware',
            ],

            'AUTH_USER_MODEL': 'user.User',

            'INSTALLED_APPS': [
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django_admin_bootstrapped',
                'django.contrib.admin',
                'django.contrib.admindocs',
                'django.contrib.admin',
                'django.contrib.admindocs',
                'app.user',
                'south',
                'app.content',
                'app.bootstrap_toolkit',
                'django_extensions',
            ],
            
            "LOGIN_URL": "/signin",
            "LOGIN_REDIRECT_URL": "/",
            "FUNC_INIT_DOWNLOAD_AMOUNT": lambda: random.randint(5000, 9999),
            "ALWAYS_ALLOWED_PERMS": ("signout/$", "signin/$"),

            
        }
    )
    ugettext = lambda s: s


def check_settings(settings):
    pass

