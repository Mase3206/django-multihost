from __future__ import annotations

from deploy_raw import exceptions

from deploy_raw.conf import StackConf



class Deployment:
	def __init__(self, stack: StackConf):
		self.stack = stack


	