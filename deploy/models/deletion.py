# from django.db.models.signals import pre_delete
# from .compose import Deployment
# from .services import Gunicorn, Postgres
# from .services.parts import *
	




def full_delete_gunicorn(gunicorn, using):
	gvols = gunicorn.volumes.all()
	for gv in gvols:
		print(f'Removing relation to {str(gv)}', end='')
		gunicorn.volumes.remove(gv)
		print(f' - deleting {str(gv)}')
		gv.delete()

	gnets = gunicorn.networks.all()
	for gn in gnets:
		print(f'Removing relation to {str(gn)}', end='')
		gunicorn.networks.remove()
		if not gn.external:
			print(f' - deleting {str(gn)}')
			gn.delete()
		else:
			print(f' - skipping deletion of {str(gn)}, as it is an external network')
	
	genvs = gunicorn.environment.all()
	for ge in genvs:
		print(f'Removing relation to {str(ge)}', end='')
		gunicorn.environment.remove()
		print(f' - deleting {str(ge)}')
		ge.delete()
	
	glabels = gunicorn.labels.all()
	for gl in glabels:
		print(f'Removing relation to {str(gl)}', end='')
		gunicorn.labels.remove()
		print(f' - deleting {str(gl)}')
		gl.delete()

	gunicorn.delete()


def full_delete_postgres(postgres, using):
	pvols = postgres.volumes.all()
	for pv in pvols:
		print(f'Removing relation to {str(pv)}', end='')
		postgres.volumes.remove(pv)
		print(f' - deleting {str(pv)}')
		pv.delete()

	pnets = postgres.networks.all()
	for pn in pnets:
		print(f'Removing relation to {str(pn)}', end='')
		postgres.networks.remove()
		if not pn.external:
			print(f' - deleting {str(pn)}')
			pn.delete()
		else:
			print(f' - skipping deletion of {str(pn)}, as it is an external network')
	
	penvs = postgres.environment.all()
	for pe in penvs:
		print(f'Removing relation to {str(pe)}', end='')
		postgres.environment.remove()
		print(f' - deleting {str(pe)}')
		pe.delete()
	
	plabels = postgres.labels.all()
	for pl in plabels:
		print(f'Removing relation to {str(pl)}', end='')
		postgres.labels.remove()
		print(f' - deleting {str(pl)}')
		pl.delete()

	postgres.delete()


def full_delete_deployment(sender, instance, using, *args, **kwargs):
	print(f'Deleting {str(instance)}')

	print(f'Deleting {str(instance.sgi_server)}')
	full_delete_gunicorn(
		instance.sgi_server, 
		using
	)
	
	print(f'Deleting {str(instance.database)}')
	full_delete_postgres(
		instance.database,
		using
	)




	

