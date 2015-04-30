# coding=utf-8
import os, sys
import random

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))

from menu import Menus, New_Menus, FRESH_MENU


def load_settings(settings, debug=True, **kwargs):
    settings.update(
        {
            'PUSH_SERVER': '10.103.88.63',
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
            'DOWNLOAD_URL': "http://dl.m.youku.com/g/",
            'SOURCE_DOWNLOAD_URL': "http://admin.gamex.mobile.youku.com/apkdownload/",
            'CHINA_CACHE_DOWNLOAD_URL': "http://dl.g.youku.com/",
            'APK_UPLOAD_PATH': "/opt/data/download",
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
            # "STATIC_ROOT": os.path.join(PROJECT_ROOT, 'statics'),
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
                'app.middleware.user_path_middleware.UserPathMiddleware',
            ],

            'AUTH_USER_MODEL': 'user.User',

            'INSTALLED_APPS': [
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                # 'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django_admin_bootstrapped',
                'django.contrib.admin',
                'django.contrib.admindocs',
                'django.contrib.admin',
                'django.contrib.admindocs',
                'app.user',
                'south',
                'app.permission',
                'app.content',
                'app.bootstrap_toolkit',
                # 'object_log',
                'django_extensions',
                #'guardian',
            ],
            "LOGIN_URL": "/signin",
            "LOGIN_REDIRECT_URL": "/",
            "MENU_CONFIG": Menus,
            "NEW_MENU_CONFIG": New_Menus,
            "FRESH_MENU_CONFIG": FRESH_MENU,
            "FUNC_INIT_DOWNLOAD_AMOUNT": lambda: random.randint(5000, 9999),
            "ALWAYS_ALLOWED_PERMS": ("signout/$", "signin/$"),

            # 是否需要同步蓝汛
            "CHINA_CACHE_PASS": False,
            "PAY_SECRTY_KEY": 'b2bde3024d5584d843329062df0c3882',
            "PAY_PUB_KEY": 'A001',
            "PAY_HOST": 'premium.paycenter.youku.com',
            "GUODO_SMS_ACCOUNT": 'youku5',
            "GUODO_SMS_PASSWORD": 'youkuku',

            'IOS_GAME_HOST': 'http://test.ios.gamex.mobile.youku.com',
            'IOS_GAME_PATH': '/app/ios_detail',
            'ANDROID_GAME_HOST': 'http://test.gamex.mobile.youku.com',
            'ANDROID_GAME_PATH': '/v2/app/detail',
            'PID_PATH': '//interface/client/pids',
            'PID_HOST': 'http://cms.m.youku.com',
            'MOBILE_API_HOST': 'http://api.mobile.youku.com',
            'MOBILE_API_OLD_HOST': 'http://api.3g.youku.com',
            # for test (in my_settings:)
            # 'MOBILE_API_HOST': 'http://test1.api.3g.youku.com',
            # 'MOBILE_API_OLD_HOST': None,
        }
    )
    ugettext = lambda s: s


def check_settings(settings):
    pass

