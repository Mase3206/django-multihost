from . import (
	BASE_DIR,
	DOCKER_BASE_DIR,
	env
)

DEPLOY_START_PORT = 8000

if env.bool('DMH_DOCKER', default=False):
	DEPLOY_DATA_ROOT = DOCKER_BASE_DIR / 'deploydata'
else:
	DEPLOY_DATA_ROOT = BASE_DIR / 'deploydata'

DEPLOY_VOL_ROOT = DEPLOY_DATA_ROOT / 'volumes'
DEPLOY_COMPOSE_ROOT = DEPLOY_DATA_ROOT / 'compose'
