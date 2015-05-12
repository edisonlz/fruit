#coding=utf-8
import sys
import os.path

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))

from django.core.management import execute_from_command_line
from django.conf import settings as django_settings
from django.utils import importlib


def execute(*modules):
    load_django_settings(*modules)
    execute_from_command_line()


def load_django_settings(*modules):
    settings = {'MODULES': modules}
    kwargs = {}
    mods = []

    for module in modules:
        #try:
        mods.append(importlib.import_module('%s.settings' % module))
        #except ImportError, err:
        #raise ImportError("Could not import settings '%s' (Is it on sys.path?): %s" % (module, err))

    for module in modules:
        try:
            mods.append(importlib.import_module('%s.my_settings' % module))
        except ImportError:
            pass

    for mod in mods:
        if hasattr(mod, 'inti_params'):
            kwargs.update(getattr(mod, 'inti_params')())

    for mod in mods:
        if hasattr(mod, 'load_settings'):
            getattr(mod, 'load_settings')(settings, **kwargs)

    for mod in mods:
        if hasattr(mod, 'check_settings'):
            getattr(mod, 'check_settings')(settings)

    django_settings.configure(**settings)


def load_settings(settings, debug=False, **kwargs):
    ugettext = lambda s: s

    settings.update({

        'SPHINXES': {
            "host": '10.105.88.62',
            "port": 9312,
            "maxmatches": 200
        },
        'redis_settings': {
            "REDIS_BACKEND": {"servers": '10.105.28.41', "port": 6379, "db": 11},
            "MQUEUE_BACKEND": {"servers": '10.105.28.41', "port": 6379, "db": 12},
            "MASTER_REDIS": {"servers": '10.105.28.41', "port": 6379, "db": 9},
            "SLAVE_REDIS": {"servers": '10.105.28.41', "port": 6379, "db": 9},
        },
        'DEBUG': debug,
        'TEMPLATE_DEBUG': debug,
        'CACHES': {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
                'LOCATION': '127.0.0.1:11211',
                # 'LOCATION': [
                #     "10.105.28.131:11211", "10.105.28.132:11211", '10.105.28.133:11211', '10.105.28.134:11211',
                #     ],
                'TIMEOUT': 0,
                'OPTIONS': {},
                }
        },
        #temporarily set to '*'
        'ALLOWED_HOSTS': ['*'],
        # 'ALLOWED_HOSTS': ['.cms.youku.com', 'localhost'],
        #先设置为一天
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'cms_platform', # Or path to database file if using sqlite3.
                'USER': 'root', # Not used with sqlite3.
                'PASSWORD': '', # Not used with sqlite3.
                'HOST': 'localhost', # Set to sempty string for localhost. Not used with sqlite3.
                'PORT': '', # Set to empty string for default. Not used with sqlite3.
                # 'CONN_MAX_AGE': 1*24*60*60,
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB'#,  SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED, autocommit=1, names "utf8";'
                    ,
                    },
                }
        },
        #'DISABLE_TRANSACTION_MANAGEMENT' : True,
        'LANGUAGES': [
                ('en', ugettext('English')),
                ('zh-cn', ugettext('Chinese')),
                                           ],

        'TRANSMETA_DEFAULT_LANGUAGE': 'zh-cn',
        'TIME_ZONE': 'Asia/Shanghai',
        'LANGUAGE_CODE': 'zh_cn',
        'SITE_ID': 1,
        'USE_I18N': True,
        'USE_L10N': True,
        'MEDIA_ROOT': '',
        'MEDIA_URL': '',
        'STATIC_ROOT': '',
        'STATIC_URL': '/static/',
        '': '/static/admin/',
        'STATICFIADMIN_MEDIA_PREFIXLES_FINDERS': [
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
        ],
        #'TEMPLATE_DIRS': (os.path.join(PROJECT_ROOT, "templates"),),
        'SECRET_KEY': 'ovvxvaacf_gx7$ldaasbn+l2asdfaadfdsafasdf2##sdfs',
        'TEMPLATE_LOADERS': (
                ('django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                )),
            ),

        'MIDDLEWARE_CLASSES': [
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.transaction.TransactionMiddleware',
            ],
        'AUTHENTICATION_BACKENDS': (
            "django.contrib.auth.backends.ModelBackend",
           # "app.user.backends.LDAPBackend",
            ),
        'TEMPLATE_CONTEXT_PROCESSORS': (
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.request",
            'django.core.context_processors.static',
            "django.contrib.auth.context_processors.auth",),

        'ROOT_URLCONF': 'base.urls',
        'INSTALLED_APPS': [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django_admin_bootstrapped',
            'django.contrib.admin',
            'django.contrib.admindocs',
            ],
        'DATE_FORMAT': 'Y-m-d',
        'DATETIME_FORMAT': 'Y-m-d H:i',
        'TIME_FORMAT': 'H:i',



        "memcache_settings": {
            "func_cache": ["localhost:11211"],
        },

        'cache_expire_2H': 60 * 60 * 2,
        'cache_expire_1H': 60 * 60,
        'cache_expire_15M': 60 * 15,
        'cache_expire_30M': 60 * 30,
        'cache_expire_1M': 60,

        }, )


