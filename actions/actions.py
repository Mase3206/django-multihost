#!/usr/bin/env python3.12
'''
Base actions.
'''
__author__ = 'Noah S. Roberts'
__license__ = 'GPLv3'


# from .helpers import *
from . import helpers


import subprocess
from argparse import Namespace
from os import getcwd, path
from textwrap import dedent


def start(args: Namespace):
	"""
	Start the specified stack.
	"""
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'up', '-d']
	helpers.runCommand(args, command)


def stop(args: Namespace):
	"""
	Stop the specified stack.
	"""
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'down']
	helpers.runCommand(args, command)


def restart(args: Namespace):
	"""
	Restart the specified stack.
	"""
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'restart']
	helpers.runCommand(args, command)


def status(args: Namespace):
	"""
	Get the status of the specified stack. If '-j' is passed, status will be printed as JSON data.
	"""
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'ps']
	if args.asJson:
		command += ['--format', 'json']
		out = helpers.runCommand(args, command, toStdOut=True, quiet=True)
		# sends output of `docker compose ps status` to `jq` for formatting
		subprocess.run('jq', input=out.stdout, encoding='UTF-8') #type:ignore
	else:
		helpers.runCommand(args, command)


def execute(args: Namespace):
	"""
	Execute a command in the given stack and service (container).
	"""
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'exec', args.service] + args.command + args.subargs
	helpers.runCommand(args, command)


def manage(args: Namespace):
	"""
	Run manage.py in the group's Gunicorn server
	"""
	args.stack = 'site'
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'exec', 'gunicorn', 'python', 'manage.py'] + args.command
	if args.subargs:
		command += args.subargs
		
	helpers.runCommand(args, command)


def build(args: Namespace):
	"""
	Build the Docker image(s) used in the stack.
	"""
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'build']
	if args.service:
		command.append(args.service)
	
	helpers.runCommand(args, command)


def pull(args: Namespace):
	"""
	Pull the latest Docker image(s) used in the stack.
	"""
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'pull']
	if args.service:
		command.append(args.service)

	helpers.runCommand(args, command)


def logs(args: Namespace):
	"""
	Display the logs of the given stack and, optionally, service. If args.follow == True, Docker will follow the log's output.
	"""
	command = ['docker', 'compose', '-f', helpers.composeStackFile(args.stack), 'logs']
	if args.follow:
		command.append('--follow')
	if args.service:
		command.append(args.service)

	helpers.runCommand(args, command)



def _validateRepo(url: str):
	"""
	Used by prep to check if the repo URL is a valid http(s) Git url. Does not check if said URL actually resolves to anything.
	"""
	urlSplit = url.split('/')
	if len(urlSplit) >= 5:
		return urlSplit[0] == 'http:' or urlSplit[0] == 'https:'
	else:
		return False



def prep(args: Namespace):
	"""
	Makes sure all required files are in this folder, then creates the '.env' file containg settings for Docker Compose, Gunicorn, and PostgreSQL.
	"""
	
	args.stack = 'site'
	thisFolder = getcwd()

	# get hostname
	thisHostname = "this server's hostname"
	try:
		thisHostnameOut = helpers.runCommand(args, ['hostnamectl', '--static'], toStdOut=True, quiet=True)
		if (
			thisHostnameOut.stdout == ''  		#type:ignore
			or thisHostnameOut.stdout == ' '  	#type:ignore
			or thisHostnameOut.stdout == '\n' 	#type:ignore
		): 
			# found hostname is empty, setting to placeholder
			thisHostname = "this server's hostname"
		else:
			thisHostname = thisHostnameOut.stdout[:-1] #type:ignore
	
	# non-linux hosts (which you SHOULDN'T USE!) won't have the `hostnamectl` command. Some linux hosts might lack them, too
	except FileNotFoundError:
		pass

	

	# check files and folders
	shouldExist_files = ['docker-compose.site.yml', 'instructions.md']
	shouldExist_folders: list[str] = []

	print('Making sure all the right folders and files are present... ')
	for fileName in shouldExist_files:
		if not path.isfile(thisFolder + '/' + fileName): 
			raise FileNotFoundError(f'Required file {fileName} not present in group folder {thisFolder}.')
		else:
			print(f"  - found {fileName}")
	
	for folderName in shouldExist_folders:
		if not path.isdir(thisFolder + '/' + folderName):
			raise helpers.DirectoryNotFoundError(f'Required folder {folderName} is not present in group folder {thisFolder}.')
		else:
			print(f"  - found {folderName}/")
	print('Found them all!\n')


	# clone repo
	if not args.gitRepo:
		repoIsValid = False
		while not repoIsValid:
			gitRepo = input("Enter the full URL to your group's GitHub repo: ")
			repoIsValid = _validateRepo(gitRepo)
			if not repoIsValid: print('Repo is not a valid url.', end=' ')
	else:
		gitRepo = args.gitRepo
	
	print('Cloning repo...')
	helpers.runCommand(args, ['rm', '-rf', 'site'], quiet=True)
	subprocess.run(['git', 'clone', gitRepo, 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

	
	# detect django project folder name
	if not args.pfName:
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
		
		# set manually if detection fails
		if not found:
			pfName = input('Django project folder not detected automatically in the site folder. Please enter the name of the Django project folder (ex: django_project, dj): ')
			while not path.isdir(thisFolder + '/site/' + pfName):
				pfName = input('Given Django project folder does not exist in the site folder. Please enter the name of the Django project folder (ex: django_project, dj): ')
				
	else:
		pfName = args.pfName

	
	# set group name
	if not args.groupName:
		groupName = input('Enter the name of your group. It should be the name of this folder: ')
	else:
		groupName = args.groupName


	# set site name
	if not args.siteName:
		siteName = input("Enter the name of your site (ex: takethebus, spaceweather, etc.). Keep it simple, as this will be in your site's URL! : ")
	else:
		siteName = args.siteName


	# review .env details before writing
	print(f'\n---\nGroup name: {groupName}')
	print(f'Site name: {siteName}')
	print(f'Django project folder: {pfName} {'(detected automatically)' if auto else ''}')
	print(f'Git repo URL: {gitRepo}\n---\n')

	if helpers.proceed(args, 'Confirm these setttings?'):
		# generate postgres password
		postgresPassword = helpers.runCommand(args, ['pwgen', '32', '1'], toStdOut=True, quiet=True).stdout #type:ignore
		djangoSecret = helpers.runCommand(args, ['pwgen', '50', '1'], toStdOut=True, quiet=True).stdout #type:ignore
		# call dedent to remove any indentations in this multi-line f-string
		envConf = dedent(
			f"""\
			GROUP_NAME={groupName}

			SITE_NAME={siteName}
			# may be called 'django', 'django_site', 'django_project', 'dj', etc.
			SITE_FOLDER={pfName}

			POSTGRES_PASSWORD={postgresPassword}

			SECRET_KEY={djangoSecret}
   			DEBUG=0  # set to '1' to enable debug mode
			"""
		)

		# write .env file
		print("Writing configuration to '.env'...", end=' ')
		with open(thisFolder + '/.env', 'w+') as envFile:
			envFile.write(envConf)
		print('done!')

		print(f"Make sure you add {thisHostname} to the ALLOWED_HOSTS list in settings.py!")

	else:
		print('Canceling!')
		exit(1)



if __name__ == '__main__':
	print('This file is not meant to be ran directly.')
	exit(2)
