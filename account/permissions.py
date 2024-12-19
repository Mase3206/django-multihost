from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from sites.models import Site



site_content_type = ContentType.objects.get_for_model(Site)



SITE_CREATE = {
	'create': Permission(
		codename='can_create',
		
	)
}
