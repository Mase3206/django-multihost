from __future__ import annotations

from deploy import exceptions
from deploy.control.mixins import DockerBuildMixin
from deploy.helpers import randomString
from deploy.conf.service.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Port,
	Label,
)
from deploy.conf.service import (
	ServiceConf
)
from deploy.conf.service import (
	DBConf
)





class SiteConf(ServiceConf, DockerBuildMixin):
	image = 'mase3206/gunicorn'

	dockerfile = './deploy/dockerfiles/gunicorn.Dockerfile'
	tag = 'v0.2'
	context = './deploy/dockerfiles/'

	def __init__(self, groupName: str, sitePath: str, projectFolder: str, database: DBConf, secretKey='', debug=False, *args, **kwargs):
		super().__init__('gunicorn', 'Mase3206/gunicorn')
		self.sitePath = sitePath
		self.projectFolder = projectFolder
		self.database = database
		if secretKey == '':
			self.secretKey = randomString(40)
		else:
			self.secretKey = secretKey
		self._debug = debug

	
	@property
	def debug(self) -> int:
		return int(self.debug)



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

