def load_settings(settings):
    settings.update({
        'DEBUG':True,
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                 #'NAME': 'cms_platform', # Or path to database file if using sqlite3.
                'NAME': 'fruit_cms_platform', # Or path to database file if using sqlite3.
                'USER': 'root', # Not used with sqlite3.
                'PASSWORD': '', # Not used with sqlite3.
                'HOST': '127.0.0.1', # Set to sempty string for localhost. Not used with sqlite3.
                'PORT': '', # Set to empty string for default. Not used with sqlite3.
    #'CONN_MAX_AGE': 1*24*60*60,
                'OPTIONS': {
                     'init_command': 'SET GLOBAL  TRANSACTION ISOLATION LEVEL READ COMMITTED;',
                },
            }
        },

        'AUTHENTICATION_BACKENDS': (
            "django.contrib.auth.backends.ModelBackend",
        ),

        "memcache_settings": {
            "func_cache": ["localhost:11211"],
            "page_cache": ["localhost:11211"],
            "fragment_cache": ["localhost:11211"],
            "user_cache": ["localhost:11211"],
        },
    })
