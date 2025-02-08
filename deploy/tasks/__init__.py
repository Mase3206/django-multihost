from django.conf import settings
from pathlib import Path
"""
- DEPLOY_VOL_ROOT
- DEPLOY_COMPOSE_ROOT
"""
DEPLOY_VOL_ROOT = Path(settings.DEPLOY_VOL_ROOT)
DEPLOY_COMPOSE_ROOT = Path(settings.DEPLOY_COMPOSE_ROOT)

from sites.models import Site

from deploy.forms.quickcreate import QuickcreateCreationMultiForm
from deploy.models import Deployment
from deploy.models.services import (
	Gunicorn,
	Postgres
)
from deploy.models.services.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Label,
)
from deploy.helpers import random_string