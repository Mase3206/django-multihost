from deploy.conf import (
	StackConf,
)
from deploy.conf.service import (
	SiteConf,
	PostgresConf,
)


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

print(repr(stack))
