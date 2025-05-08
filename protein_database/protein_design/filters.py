import django_filters
from .models import *
from django.db.models import Q
from django import forms
from django import template




class AssayFilter(django_filters.FilterSet):
    # Global search geral
    global_search = django_filters.CharFilter(method='filter_global', label='Busca geral')

    sp = django_filters.ModelChoiceFilter(
        field_name='fk_id_category__specificproperty',
        queryset=SpecificProperty.objects.all(),
        label='Specific Property'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['sp'].field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Propriedade específica'})

    
    fk_id_techniques = django_filters.ModelChoiceFilter(
        queryset=UsedTechnique.objects.all(),
        label='Técnica'
    )

    design_type = django_filters.ChoiceFilter(
    field_name='fk_id_design__design_type',
    choices=Design._meta.get_field('design_type').choices,
    label='Design Type'
    )

    technique_type = django_filters.ChoiceFilter(
        field_name='fk_id_techniques__technique_type',
        choices=UsedTechnique._meta.get_field('technique_type').choices,
        label='Tipo de Técnica'
    )

    success_validation = django_filters.ChoiceFilter(
        field_name='success_validation',
        choices=[
            (True, 'Sim'),
            (False, 'Não')
        ],
        label='Validação bem-sucedida'
    )

    class Meta:
        model = Assay
        fields = ['fk_id_category', 'fk_id_design', 'fk_id_techniques']

    def filter_global(self, queryset, name, value):
        return queryset.filter(
            Q(assay_name__icontains=value) |
            Q(fk_id_design__design_name__icontains=value) |
            Q(fk_id_design__pdb_id__icontains=value) |
            Q(fk_id_design__organism__icontains=value) |
            Q(fk_id_design__design_type__icontains=value)
        )