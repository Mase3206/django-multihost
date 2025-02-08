

from environs import Env

env = Env()
env.read_env()

FORCE_SCRIPT_NAME = (
	'/' + env.str('SITE_PATH', default='') 
	if env.str('SITE_PATH', default='') != '' 
	else ''
)


LOGIN_URL = FORCE_SCRIPT_NAME + LOGIN_URL
STATIC_URL = FORCE_SCRIPT_NAME + '/static/'

MEDIA_URL = FORCE_SCRIPT_NAME + '/media/'
if FORCE_SCRIPT_NAME != '':
	MEDIA_SERVE_URL = '/'.join(MEDIA_URL.split('/')[2:])
else:
	MEDIA_SERVE_URL = MEDIA_URL

MEDIA_ROOT = BASE_DIR / 'media'

DATABASES = {
	# PostgreSQL database used with dmh
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': env.str('POSTGRES_DB', default=None),
		'USER': env.str('POSTGRES_USER', default=None),
		'PASSWORD': env.str('POSTGRES_PASSWORD', default=None),
		'HOST': 'postgres',
		'PORT': '5432',
	},
}
