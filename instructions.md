# Deployment Instructions

## Preparing your Django project

### requirements.txt

Make sure Whitenoise v6.8 or higher is installed in your virtual environment and defined in your requirements.txt file. v6.7 does not serve static files at all ([see issue](https://github.com/Mase3206/django-multihost/issues/5)).

```shell
pip uninstall whitenoise
pip install whitenoise~=6.8
```


```txt
# requirements.txt
# replace existing whitenoise line with this
whitenoise~=6.8
```


### settings.py

In your 'settings.py' file, add these lines in the specified locations.

> [!WARNING]
> Make sure you copy this stuff ***exactly* how it is**. MultiHost expects these fields to be set as they are below. If you ever get an error about unknown/missing paths, invalid url configs, database stuff, or missing static files, check here.

- Add these imports
```python
import os
```


- Place this after BASE_DIR is set
```python
# make sure you import the `os` module!
FORCE_SCRIPT_NAME = (
    "/" + os.environ.get("SITE_NAME", "")     # if the SITE_NAME env variable is set
    if os.environ.get("SITE_NAME", "") != ""  # if not
    else ""	                                  # set to nothing to let Django take over
)
```


- Set DEBUG to False; this is a "production" environment, and we don't want our precious insider knowledge leaking out, now do we?
```python
DEBUG = bool(int(os.environ.get(
	'DEBUG', 
	False  # or True, to fail unsafely
)))
```


- Modify existing elements in these two lists
```python
ALLOWED_HOSTS = [
	'localhost',
	'127.0.0.1',
	'csci258.cs.umt.edu',  # this is the url of the VM
]
INTERNAL_IPS = [
	'127.0.0.1',
	'localhost',
]
```


- Put these two middlewares in this order
```python
MIDDLEWARE = [
	# ... 
	'django.middleware.security.SecurityMiddleware', # already exists
	'whitenoise.middleware.WhiteNoiseMiddleware',    # this *must* go right after the one above
	# ...
]
```


- Replace your existing database configs with this (unless you have a third one used for a specific test case, then just leave that)
```python
DATABASES = {
	# PostgreSQL database used in production
	'prod': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('POSTGRES_DB'),
		'USER': os.environ.get('POSTGRES_USER'),
		'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
		'HOST': 'postgres',
		'PORT': '5432',
	},

	# local SQLite database used for development and testing
	'local': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}

	# any other configs would go down here
}


# defaults to local if not set in environment variable
# environment variable is set by the Docker config
default_database = os.environ.get('DJANGO_DATABASE', 'local')
# sets detected database to default
DATABASES['default'] = DATABASES[default_database]
```


- Replace your static files settings with *exactly* this
```python
# URL path to serve static files from; ex: '/group1/static/'
STATIC_URL = FORCE_SCRIPT_NAME + '/static/'
# project static files location
STATICFILES_DIRS = [ BASE_DIR / "static" ]
# collected static files location; includes other apps, like admin
STATIC_ROOT = BASE_DIR / 'staticfiles'
# enable caching and compression when serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---
#### Secrets

You'll need a way to store some secrets that shouldn't be committed to Git. While this is by no means the only way, this is the way I would start with.

- In your 'settings.py', change the Django SECRET_KEY so it loads from a secrets file. Here's an example:
```python
# load the key; use default if key var not set
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4$6@5&r4%kex2%me935-8q^=ep=ufnyv89&i7@dx^68924o2q#')
```

Don't worry about generating this key manually, as `deploy prep` generates it and adds it to '.env' for you.


## Setting up the environment

More examples can be found on [the Wiki](https://github.com/Mase3206/django-multihost/wiki/Examples#groups).

1. Use SSH (**S**ecure **Sh**ell) to open a remote terminal into the class VM. Like above, replace `username` with the username given to you.
```bash
ssh username@csci258.cs.umt.edu
```

2. Use `cd` to navigate to your group's directory. Like above, replace `GROUP_NAME` with your group's actual name.
```bash
cd /django/TERM/GROUP_NAME
# example:
cd /django/fall24/group1
```

3. **Before doing *anything* else,** Run the following command to set up your group's environment. It'll walk you through a couple steps.
```bash
deploy prep
```

## Deploying your site

Thankfully, deployment is super simple. I've made a helpful script, `deploy`, to simplify dealing with Docker Compose. Once you and your group have done everything above, run:
```bash
deploy start site
```

To see its status, run:
```bash
deploy status site
```
This displays the standard Docker Compose output style, as that's what's running under the hood. In fact, the command being run is:
```bash
# the last command under the hood
docker compose -f docker-compose.site.yml ps
```

To take down your site, run:
```bash
deploy stop site
```


## Running commands inside the site

Generally, commands can be run in either the Gunicorn or PostgreSQL Docker containers with the following syntax:
```bash
# under the hood
docker compose -f docker-compose.site.yml exec (container) (command) [args...]
```
However, with `deploy`, it's a bit simpler:
```bash
deploy exec site (container) (command) [args...]
```

Because your Django site is being served by a Docker container running the Gunicorn WSGI server, running commands with 'manage.py' is a little more complex. Without `deploy`, you would have to run:
```bash
# under the hood
docker compose -f docker-compose.site.yml exec gunicorn python manage.py (command) [args...]
```
...which is gross. Instead, you can use 'manage.py' like so:

```bash
deploy manage [commands...]
```

In this environment, it would likely only be used to create the superuser, as that is tied to the database, and the production database is different from the one used for local testing.

> [!NOTE]
> **Fun fact:** The all-important `deploy` command is just another Python script. If you run the command "`which deploy`" in the terminal, you'll see it's located at '/usr/local/bin/deploy', which is a symlink (kinda like a Windows short cut, just like a macOS alias) to '/django/source/deploy.py'. 
