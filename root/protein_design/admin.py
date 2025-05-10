from django.contrib import admin

# Register your models here.
from .models import Category, Design, Protocol, UsedTechnique, Assay, ComputationalResult, ExperimentalResult, Sequence, SpecificProperty, Unit, UnitHasSpecificProperty

admin.site.register(Category)
admin.site.register(Design)
admin.site.register(Protocol)
admin.site.register(UsedTechnique)
admin.site.register(Assay)
admin.site.register(ComputationalResult)
admin.site.register(ExperimentalResult)
admin.site.register(Sequence)
admin.site.register(SpecificProperty)
admin.site.register(Unit)
admin.site.register(UnitHasSpecificProperty)