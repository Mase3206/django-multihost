#!/usr/bin/env python3

import argparse
import subprocess
from os import getcwd, listdir, path
from textwrap import dedent

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
	print(f'Using {composeFile}')
	return path.exists(composeFile)

def getStacksInDir() -> list[str]:
	"""Get the Docker Compose files (stacks) in the current directory."""
	listing = listdir(getcwd())
	stacks = []

	for l in listing:
		if len(ls := l.split('.')) >= 3 \
				and ls[0] == 'docker-compose' \
				and ls[2] == ('yml' or 'yaml'):
			stacks.append(ls[1])
	
	return stacks

def getServicesInStack(stack: str) -> list[str]:
	"""Get the service names defined in the given stack."""
	with open(composeStackFile(stack), 'r') as f:
		dcf: dict[str, dict[str, dict]] = yaml.safe_load(f)
	
	services = list(dcf['services'].keys())
	return services


def runCommand(args: argparse.Namespace, command: list):
	"""
	Check if the stack given via CLI exists, then run the given command list via `subprocess.run()`, printing an error if the stack does not exist.

	Arguments
	---------
		args (argparse.Namespace) : parsed command-line arguments from `argparse`
		command (list) : command list containing the program name and all arguments
	"""
	if checkComposeStackExists(args.stack):
		subprocess.run(command)
	else:
		print(f'Docker compose file {composeStackFile(args.stack)} for stack {args.stack} is not present in the current directory.')
		exit(2)

def proceed(message: str, default=True) -> bool:
	"""
	Ask the user if they would like to proceed using the given message.

	Arguments
	---------
		message (str) : message to display to user
		default (bool) : default option; True = yes, False = no
	"""
	if default == True:
		choices = ' [Y/n] '
	else:
		choices = ' [y/N] '

	resp = input(message + choices)

	if default == True:
		if resp.lower() == ('y' or 'yes' or ''):
			return True
		else:
			return False
	else:
		if resp.lower() == ('y' or 'yes'):
			return True
		else:
			return False



def start(args: argparse.Namespace):
	command = ['docker', 'compose', '-f', composeStackFile(args.stack), 'up', '-d']
	runCommand(args, command)


def stop(args: argparse.Namespace):
	command = ['docker', 'compose', '-f', composeStackFile(args.stack), 'down']
	runCommand(args, command)


def status(args: argparse.Namespace):
	command = ['docker', 'compose', '-f', composeStackFile(args.stack), 'ps']
	runCommand(args, command)


def execute(args: argparse.Namespace):
	command = ['docker', 'compose', '-f', composeStackFile(args.stack), 'exec', args.service, args.command] + args.subargs
	runCommand(args, command)


def manage(args: argparse.Namespace):
	args.stack = 'site'
	command = ['docker', 'compose', '-f', composeStackFile(args.stack), 'exec', 'gunicorn', 'python', 'manage.py'] + args.subargs
	runCommand(args, command)


def build(args: argparse.Namespace):
	command = ['docker', 'compose', '-f', composeStackFile(args.stack), 'build']
	if args.service:
		command.append(args.service)
	
	runCommand(args, command)


def logs(args: argparse.Namespace):
	command = ['docker', 'compose', '-f', composeStackFile(args.stack), 'logs']
	if args.follow:
		command.append('--follow')
	if args.service:
		command.append(args.service)

	runCommand(args, command)



def prep(args: argparse.Namespace):
	"""
	Makes sure all required files are in this folder, then creates the '.env' file containg settings for Docker Compose, Gunicorn, and PostgreSQL.
	"""
	args.stack = 'site'
	# command = ['docker']
	thisFolder = getcwd()
	shouldExist_files = ['docker-compose.site.yml', 'deploy.py']
	shouldExist_folders = ['site', ]

	print('Making sure all the right folders and files are present... ')
	for fileName in shouldExist_files:
		if not path.isfile(thisFolder + '/' + fileName): 
			raise FileNotFoundError(f'Required file {fileName} not present in group folder {thisFolder}.')
		else:
			print(f"  - found {fileName}")
	
	for folderName in shouldExist_folders:
		if not path.isdir(thisFolder + '/' + folderName):
			raise DirectoryNotFoundError(f'Required folder {folderName} is not present in group folder {thisFolder}.')
		else:
			print(f"  - found {folderName}/")
	print('Found them all!\n')


	expectedProjectFolders = ['django', 'django_site', 'django_project', 'dj']
	pfName = ''
	found = False
	auto = False
	for pf in expectedProjectFolders:
		found = path.isdir(thisFolder + '/site/' + pf)
		if found:
			auto = True
			pfName = pf
			break
	
	if not found:
		pfName = input('Django project folder not detected automatically in the site folder. Please enter the name of the Django project folder (ex: django_project, dj): ')

	
	groupName = input('Enter the name of your group. It should be the name of this folder: ')
	siteName = input("Enter the name of your site (ex: takethebus, spaceweather, etc.). Keep it simple, as this will be in your site's URL! : ")


	print(f'\nGroup name: {groupName}')
	print(f'Site name: {siteName}')
	print(f'Django project folder: {pfName} {'(detected automatically)' if auto else ''}\n')

	if proceed('Confirm these setttings?'):
		envConf = dedent(
			f"""\
			GROUP_NAME={groupName}

			SITE_NAME={siteName}
			# may be called 'django', 'django_site', 'django_project', 'dj', etc.
			SITE_FOLDER={pfName}
			"""
		)
		print("Writing configuration to '.env'...", end=' ')
		with open(thisFolder + '/.env', 'w+') as envFile:
			envFile.write(envConf)
		print('done!')

	else:
		print('Canceling!')
		exit(1)



def getArgs():
	"""
	Get the command line arguments passed by the user. The return of this can be used to call the function relevant to the subparser "selected" by the user.

	Returns
	-------
		args (argparse.Namespace) : a Namespace object with the parsed arguments

	Example Usage
	-------------
	```
	args = getArgs()
	args.func(args)  # call subparser defaults
	```
	"""
	# dynamically fetch available stacks and services available to control
	stackChoices = getStacksInDir()

	serviceChoices: list[str] = []
	for stack in stackChoices:
		serviceChoices += getServicesInStack(stack)
	serviceChoices = list(set(serviceChoices))
	

	parser = argparse.ArgumentParser(description="Helpful script to manage a group's Gunicorn and PostgreSQL deployment for CSCI 258.", epilog="Author: Noah S. Roberts, 2024")

	subparsers = parser.add_subparsers(required=True)
	
	h = "Starts the specified stack."
	parser_start = subparsers.add_parser('start', description=h, help=h)
	parser_start.add_argument('stack', choices=stackChoices)
	parser_start.set_defaults(func=start)

	h = "Stops the specified stack."
	parser_stop = subparsers.add_parser('stop', description=h, help=h)
	parser_stop.add_argument('stack', choices=stackChoices)
	parser_stop.set_defaults(func=stop)

	h = "Displays the current status of the specified stack."
	parser_status = subparsers.add_parser('status', description=h, help=h)
	parser_status.add_argument('-j', dest='asJson')
	parser_status.add_argument('-r', dest='asRaw')
	parser_status.add_argument('stack', choices=stackChoices)
	parser_status.set_defaults(func=status)

	h = "Runs the specified command in the given stack and container."
	parser_exec = subparsers.add_parser('exec', description=h, help=h)
	parser_exec.add_argument('stack', choices=stackChoices)
	parser_exec.add_argument('service', choices=serviceChoices)
	parser_exec.add_argument('command', nargs=1)
	parser_exec.add_argument('subargs', nargs='*')
	parser_exec.set_defaults(func=execute)

	h = "Run manage.py with the specified arguments"
	parser_manage = subparsers.add_parser('manage', description=h, help=h)
	parser_manage.add_argument('subargs', nargs='*')
	parser_manage.set_defaults(func=manage)

	h = "Prepare your group's folder for deployment."
	parser_prep = subparsers.add_parser('prep', description=h, help=h)
	parser_prep.set_defaults(func=prep)

	h = "Build the Docker image(s) used in the stack. Not used for group deployments."
	parser_build = subparsers.add_parser('build', description=h, help=h)
	parser_build.add_argument('stack', choices=stackChoices)
	parser_build.add_argument('service', choices=serviceChoices, nargs='?')
	parser_build.set_defaults(func=build)

	h = "Display log output of the stack or one of its services."
	parser_logs = subparsers.add_parser('logs', description=h, help=h)
	parser_logs.add_argument('-f', '--follow', dest='follow', help="Follow log output", action='store_true')
	parser_logs.add_argument('stack', choices=stackChoices)
	parser_logs.add_argument('service', choices=serviceChoices, nargs='?')
	parser_logs.set_defaults(func=logs)

	return parser.parse_args()


if __name__ == '__main__':
	# collect the command line arguments
	args = getArgs()
	try:
		args.func(args)
	except KeyboardInterrupt:
		exit(1)
