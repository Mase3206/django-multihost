from betterforms.multiform import MultiModelForm

from .compose import DeploymentQuickcreateForm
from .services import (
	GunicornQuickcreateForm,
	PostgresQuickcreateForm,
)

from .parts import (
	VolumeForm,
	NetworkForm,
	EnvironmentVariableForm,
	LabelForm,
)



class QuickcreateCreationMultiForm(MultiModelForm):
	form_classes = {
		'deployment': DeploymentQuickcreateForm,
		'gunicorn': GunicornQuickcreateForm,
	}
