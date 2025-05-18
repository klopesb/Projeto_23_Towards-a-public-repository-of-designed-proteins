import django_filters
from .models import *
from django.db.models import Q
from django import forms
from django import template


class SelectWithDisabledFirstOption(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if index == 0:
            option['attrs']['disabled'] = False
        return option

class AssayFilter(django_filters.FilterSet):
    # Global search geral
    global_search = django_filters.CharFilter(method='filter_global', label='Busca geral')

    sp = django_filters.ModelChoiceFilter(
        field_name='fk_id_category__specificproperty',
        queryset=SpecificProperty.objects.all(),
        label='Specific Property',
        empty_label='No selection',
        widget = SelectWithDisabledFirstOption()
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.filters['sp'].field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Propriedade específica'})

    fk_id_category = django_filters.ModelChoiceFilter(
    queryset=Category.objects.all(),
    label='Category',
    empty_label='No selection',
    widget=SelectWithDisabledFirstOption()
    )

    fk_id_techniques = django_filters.ModelChoiceFilter(
        queryset=UsedTechnique.objects.all(),
        label='Technique',
        empty_label='No selection',
        widget = SelectWithDisabledFirstOption()
    )

    design_type = django_filters.ChoiceFilter(
    field_name='fk_id_design__design_type',
    choices=Design._meta.get_field('design_type').choices,
    label='Design Type',
    empty_label='No selection',
    widget = SelectWithDisabledFirstOption()
    )

    technique_type = django_filters.ChoiceFilter(
        field_name='fk_id_techniques__technique_type',
        choices=UsedTechnique._meta.get_field('technique_type').choices,
        label='Technique Type',
        empty_label='No selection',
        widget = SelectWithDisabledFirstOption()
    )

    success_validation = django_filters.ChoiceFilter(
        field_name='success_validation',
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ],
        label='Validação bem-sucedida',
        empty_label='No selection',
        widget = SelectWithDisabledFirstOption()
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