__author__ = 'yinxing'

def load_settings(settings, debug=True, **kwargs):
    settings.update(
        {

        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'fruit_cms_platform', # Or path to database file if using sqlite3.
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

        }
    )
