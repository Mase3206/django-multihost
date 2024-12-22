from django.conf import settings
from pathlib import Path
"""
- DEPLOY_VOL_ROOT
- DEPLOY_COMPOSE_ROOT
"""
DEPLOY_VOL_ROOT = Path(settings.DEPLOY_VOL_ROOT)
DEPLOY_COMPOSE_ROOT = Path(settings.DEPLOY_COMPOSE_ROOT)