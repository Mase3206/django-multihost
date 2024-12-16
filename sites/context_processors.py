from .models import Site


def all_sites(request):
	sites = Site.objects.all()
	return {'all_sites': sites}
