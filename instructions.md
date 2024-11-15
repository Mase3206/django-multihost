# Deployment Instructions

## Preparing your Django project

In your 'settings.py' file, add the following lines in the specified locations:


- Place this after BASE_DIR is set
```python
# make sure you import the `os` module!
FORCE_SCRIPT_NAME = '/' + os.environ.get('SITE_NAME', '')
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



- Set your databases to *exactly* this
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
}


# defaults to local if not set in environment variable
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


## Setting up the environment

<!-- 1. Use `scp` (**S**SH **C**o**p**y) to copy the contents your django site folder (the folder containing 'manage.py') into the 'sites' folder in your group's directory on the class VM.
	- Make sure to replace `SITE_FOLDER` and `GROUP_NAME` with the name of the django site folder and your group's name, respectively.
	- Replace `netid` in `netid@csci258.cs.umt.edu` with your actual NetID.
```bash
scp SITE_FOLDER/* netid@csci258.cs.umt.edu:/django/fall24/GROUP_NAME/site/*
``` -->

1. Use SSH (**S**ecure **Sh**ell) to open a remote terminal into the class VM. Like above, replace `netid` with your actual NetID.
```bash
ssh netid@csci258.cs.umt.edu
```

2. Use `cd` to navigate to your group's directory. Like above, replace `GROUP_NAME` with your group's actual name.
```bash
cd /django/TERM/GROUP_NAME
# example:
cd /django/fall24/group1
```

3. Run the following command to set up your group's environment. It'll walk you through a couple steps.
```bash
deploy prep
```

## Deploying your site

Thankfully, deployment is super simple. We've made a helpful script, 'deploy.py`, to simplify dealing with Docker Compose. Once you and your group have done everything above, run:
```bash
deploy start site
```

To see its status, run:
```bash
deploy status site
```
This displays the standard Docker Compose output style, as that's what's running under the hood. In fact, the command being run is:
```bash
docker compose -f docker-compose.site.yml ps
```

To take down your site, run:
```bash
deploy stop site
```


## Running commands inside the site

Generally, commands can be run in either the Gunicorn or PostgreSQL Docker containers with the following syntax:
```bash
docker compose -f docker-compose.site.yml exec (container) (command) [args...]
```
However, with `deploy`, it's a bit simpler:
```bash
deploy exec site (container) (command) [args...]
```

Because your Django site is being served by a Docker container running the Gunicorn WSGI server, running commands with 'manage.py' is a little more complex. Without `deploy`, you would have to run:
```bash
docker compose -f docker-compose.site.yml exec gunicorn python manage.py (command) [args...]
```
...which is gross. Instead, you can use 'manage.py' like so:

```bash
deploy manage [commands...]
```

In this environment, it would likely only be used to create the superuser, as that is tied to the database, and the production database is different from the one used for local testing.

<!-- > [!NOTE]
> **Fun fact:** When using a POSIX shell (Bash, Zsh, etc., but not any Windows shell) and if the script is set up correctly, you can actually run scripts without explicitly calling their interpreter. Thus, the above command could be run as: 
> ```bash
> ./deploy.py manage
> ``` -->

> [!NOTE]
> **Fun fact:** The all-important `deploy` command is just a Python script. If you call the command `which deploy` in the terminal, you'll see it's located at /usr/local/bin/deploy, which is a symlink (kinda like a Windows short cut, just like a macOS alias) to /django/source/deploy.py. 