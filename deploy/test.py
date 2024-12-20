from deploy.conf.base import (
	StackConf,
	SiteConf,
	PostgresConf
)


stack = StackConf('test')

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
