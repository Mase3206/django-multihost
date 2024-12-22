from . import BASE_DIR



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# URL path to serve static files from; ex: '/group-3/static/'
STATIC_URL = 'static/'
# project static files location
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
# collected static files location; includes other apps, like admin
STATIC_ROOT = BASE_DIR / 'staticfiles'
# enable caching and compression when serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'





CRISPY_TEMPLATE_PACK = 'bulma'
CRISPY_ALLOWED_TEMPLATE_PACKS = (
	'bulma',
)