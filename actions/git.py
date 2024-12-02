'''
Git actions
'''

# from .helpers import *
from . import helpers

from argparse import Namespace
from os import getcwd, chdir, path



def _gitOp(args, command, folder=''):
	if not folder:
		folder = args.folder
	
	cwd = getcwd()
	chdir(path.join(cwd, folder))
	helpers.runCommand(args, command, ignoreStack=True)
	chdir(cwd)



def pull(args: Namespace):
	command = ['git', 'pull']
	_gitOp(args, command)


def hard_reset(args: Namespace): 
	if helpers.proceed(
		args,
		"Are you sure you want to hard reset your repo? This will irreversably overwrite any and all changes made locally.",
		default=False
	):
		command = ['git', 'reset', '--hard', 'origin/HEAD']
		_gitOp(args, command)
	else:
		print('Aborting.')
