from __future__ import annotations

from deploy_raw import exceptions
from deploy_raw.control.mixins import DockerBuildMixin
from deploy_raw.helpers import randomString
from deploy_raw.conf.service.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Port,
	Label,
)
from deploy_raw.conf.service import (
	ServiceConf
)
from deploy_raw.conf.service import (
	DBConf
)





class SiteConf(ServiceConf, DockerBuildMixin):
	image = 'mase3206/gunicorn'

	dockerfile = './deploy/dockerfiles/gunicorn.Dockerfile'
	tag = 'v0.2'
	context = './deploy/dockerfiles/'

	def __init__(
			self, 
			groupName: str, 
			sitePath: str, 
			projectFolder: str, 
			database: DBConf, 
			secretKey='', 
			debug=False, 
			*args, **kwargs
		):
		super().__init__('gunicorn', 'Mase3206/gunicorn')
		self.groupName = groupName
		self.sitePath = sitePath
		self.projectFolder = projectFolder
		self.database = database
		if secretKey == '':
			self.secretKey = randomString(40)
		else:
			self.secretKey = secretKey
		self._debug = debug
		self._addParts()

	
	@property
	def debug(self) -> int:
		return int(self._debug)



	def _getProjectFolder(self):
		raise NotImplementedError()
		# expectedProjectFolders = ['django', 'django_site', 'django_project', 'dj']
		# pfName = ''
		# found = False
		# auto = False
		# for pf in expectedProjectFolders:
		# 	found = path.isdir(thisFolder + '/site/' + pf)
		# 	if found:
		# 		auto = True
		# 		pfName = pf
		# 		break
		
		# # set manually if detection fails
		# if not found:
		# 	pfName = input('Django project folder not detected automatically in the site folder. Please enter the name of the Django project folder (ex: django_project, dj): ')
		# 	while not path.isdir(thisFolder + '/site/' + pfName):
		# 		pfName = input('Given Django project folder does not exist in the site folder. Please enter the name of the Django project folder (ex: django_project, dj): ')

		# return pfName

	
	def _addParts(self):
		self.volumes += [
			Volume('./siteroot', '/sites/django'),
			Volume('./.volumes/gunicorn', '/run/www/django'),
		]
		self.environment += [
			*self.database.environment,
			EnvironmentVariable('DJANGO_DATABASE', 'prod'),
			EnvironmentVariable('SITE_PATH', self.sitePath),
			EnvironmentVariable('PROJECT_FOLDER', self.projectFolder),
			EnvironmentVariable('SECRET_KEY', self.secretKey),
			EnvironmentVariable('DEBUG', str(self.debug)),
		]
		self.labels += [
			Label('traefik.enable', 'true'),
			Label('traefik.docker.network', 'traefik'),

			# set the hostname and path
			Label(f'traefik.http.routers.gunicorn-{self.groupName}.rule', 'Host(gunicorn)'),
			Label(f'traefik.http.routers.gunicorn-{self.groupName}.rule', f'PathPrefix(`/{self.sitePath})'),

			# strip the path away and continue
			Label(f'traefik.http.routers.gunicorn-{self.groupName}.middlewares', f'gunicorn-{self.groupName}-stripprefix'),
			Label(f'traefik.http.middlewares.gunicorn-{self.groupName}-stripprefix.stripprefix.prefixes', f'/{self.sitePath}'),
		]
		self.networks += [
			Network('traefik', external=True),
			Network(f'{self.groupName}_default')
		]
