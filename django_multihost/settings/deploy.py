from pathlib import Path

DEPLOY_START_PORT = 8000

DEPLOY_DATA_ROOT = Path(__file__).resolve().parent.parent / 'deploydata'

DEPLOY_GIT_ROOT = DEPLOY_DATA_ROOT / 'git'
DEPLOY_VOL_ROOT = DEPLOY_DATA_ROOT / 'volumes'
DEPLOY_COMPOSE_ROOT = DEPLOY_DATA_ROOT / 'compose'
