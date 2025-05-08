from import_export import resources
from .models import Resultado

class ResultadoResource(resources.ModelResource):
    class Meta:
        model = Resultado
