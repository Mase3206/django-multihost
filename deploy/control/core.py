from __future__ import annotations

from deploy import exceptions

from deploy.conf import StackConf



class Deployment:
	def __init__(self, stack: StackConf):
		self.stack = stack


	