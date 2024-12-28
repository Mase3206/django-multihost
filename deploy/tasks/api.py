from typing import Any, TypedDict
from subprocess import CalledProcessError

from . import *

class Actions(TypedDict):
	actions: list[str]



def _update(depl: Deployment):
	print(f'Pulling latest code from {depl.git_repo} for {depl}')
	depl.update()

def _start(depl: Deployment):
	print(f'Starting {depl}')
	depl.up().check_returncode()

def _stop(depl: Deployment):
	print(f'Stopping {depl}')
	depl.down().check_returncode()

def _restart(depl: Deployment):
	print(f'Restarting {depl}')
	depl.restart().check_returncode()




def parse_actions(depl: Deployment, payload: Actions):
	"""
	Parse the action(s) sent via the "/deploy/api/&lt;int:deploy_id&gt;/" endpoint.

	Arguments
	---------
		depl (Deployment) : Deployment model instance to act upon.
		payload (Actions) : Request data containing the list of actions to take.

	"""


	for act in payload['actions']:
		match act:
			case 'update':  return _update(depl)
			case 'start':   return _start(depl)
			case 'stop':    return _stop(depl)
			case 'restart': return _restart(depl)

	
