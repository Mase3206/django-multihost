from deploy.conf import (
	StackConf,
	initializeFromYaml,
)
from deploy.conf.service import (
	SiteConf,
	PostgresConf,
)

import json, yaml, sys


def manual():
	stack = StackConf('test this')

	db = PostgresConf()

	stack += [
		SiteConf(
			groupName='test',
			sitePath='test',
			projectFolder='dj',
			database=db,
			# debug=True,
		),
		db
	]

	# print(repr(stack))
	return stack


def fromYaml():
	stack = initializeFromYaml('deploy/example/deploy.yml')
	print(json.dumps(stack.toDict()))

print(yaml.safe_dump(manual().toCompose()))