'''
Helper functions used by the actions module.
'''
__author__ = 'Noah S. Roberts'
__license__ = 'GPLv3'


import subprocess
import sys
from argparse import Namespace
from os import getcwd, listdir, path

import yaml


class DirectoryNotFoundError(FileNotFoundError): pass



def composeStackFile(stack: str) -> str:
	"""
	Get the Docker Compose filename for the given stack, assuming it exists.
	
	Arguments
	---------
		stack (str) : Docker Compose stack name
	"""
	return f'docker-compose.{stack}.yml'


def checkComposeStackExists(stack: str) -> bool:
	"""
	Check if the given stack's Docker Compose file exists.
	
	Arguments
	---------
		stack (str) : Docker Compose stack name
	"""
	composeFile = getcwd() + '/' + composeStackFile(stack)
	sys.stderr.write(f'Using {composeFile}\n') # write to stderr instead of stdout
	return path.exists(composeFile)


def getStacksInDir() -> list[str]:
	"""
	Get the Docker Compose files (stacks) in the current directory.
	"""
	listing = listdir(getcwd())
	stacks = []

	for l in listing:
		if len(ls := l.split('.')) >= 3 \
				and ls[0] == 'docker-compose' \
				and ls[2] == ('yml' or 'yaml'):
			stacks.append(ls[1])
	
	return stacks


def getServicesInStack(stack: str) -> list[str]:
	"""
	Get the service names defined in the given stack.
	"""
	with open(getcwd() + '/' + composeStackFile(stack), 'r') as f:
		dcf: dict[str, dict[str, dict]] = yaml.safe_load(f)
	
	services = list(dcf['services'].keys())
	return services


def runCommand(args: Namespace, command: list, toStdOut=False, quiet=False, ignoreStack=False):
	"""
	Check if the stack given via CLI exists, then run the given command list via `subprocess.run()`, printing an error if the stack does not exist.

	Arguments
	---------
		args (Namespace) : parsed command-line arguments from `argparse`.
		command (list) : command list containing the program name and all arguments.
		toStdOut (bool, False) : return the stdout and stderr of the command. Removes all formatting in the process.
		quiet (bool, False) : Do not print the output of the command.
	"""
	if not ignoreStack:
		stackExists = checkComposeStackExists(args.stack)
	else: 
		stackExists = True

	if stackExists:
		# run normally
		if not toStdOut:
			subprocess.run(command)
		# capture output
		else:
			out = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='UTF-8')
			# do not print, if desired
			if not quiet:
				print(out.stdout)
			return out
	else:
		print(f'Docker compose file {composeStackFile(args.stack)} for stack {args.stack} is not present in the current directory.')
		exit(2)


def proceed(args: Namespace, message: str, default=True) -> bool:
	"""
	Ask the user if they would like to proceed using the given message.

	Arguments
	---------
		message (str) : message to display to user
		default (bool) : default option; True = yes, False = no
	"""
	if not args.alwaysConfirm:
		if default == True:
			choices = ' [Y/n] '
		else:
			choices = ' [y/N] '

		resp = input(message + choices)

		if default == True:
			# accept an empty newline as default yes
			if resp.lower() == ('y' or 'yes' or ''):
				return True
			else:
				return False
		else:
			# treat an empty newline as default no
			if resp.lower() == ('y' or 'yes'):
				return True
			else:
				return False
			
	# bypass if -y is passed
	else:
		return args.alwaysConfirm
