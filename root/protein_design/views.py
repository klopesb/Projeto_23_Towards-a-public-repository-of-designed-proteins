from django.shortcuts import render, redirect
from django.db import transaction
import csv
import pandas as pd
from django.forms import modelformset_factory
from .filters import AssayFilter
from django.db.models import Prefetch
from .validators import *
# Create your views here.
#from django.http import HttpResponse

from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import *
from django.http import HttpResponse

#Página designs - /designs 
#Fazer uma lista com as proteinas e puxar a imagem do pdb (se der certo)
def design_list(request):
    designs = Design.objects.all()
    return render(request, 'templates/protein_design/design_list.html', {'designs': designs})

#Página de buscas  - /design_search
def design_search(request):
    assay_list = Assay.objects.all()
    assay_filter = AssayFilter(request.GET, queryset=assay_list)
    return render(request, 'templates/protein_design/design_search.html', {'filter': assay_filter})


#pagina de detalhes do design - /design/<int:id_design>

def design_detail(request, id_design):
    design = get_object_or_404(Design, id_design=id_design)

    # Prefetch unidades relacionadas às propriedades específicas da categoria de cada ensaio
    unit_prefetch = Prefetch(
        'unithasspecificproperty_set',
        queryset=UnitHasSpecificProperty.objects.select_related('fk_id_unit')
    )

    # Prefetch propriedades específicas da categoria, já com suas unidades associadas
    property_prefetch = Prefetch(
        'fk_id_category__specificproperty_set',
        queryset=SpecificProperty.objects.prefetch_related(unit_prefetch)
    )

    # Ensaios relacionados ao design com otimizações de acesso
    assays = design.assay_set.select_related(
        'fk_id_category',
        'fk_id_protocol',
        'fk_id_techniques'
    ).prefetch_related(
        property_prefetch,
        'fk_id_techniques__computationalresult_set',
        'fk_id_techniques__experimentalresult_set'
    )

    return render(request, 'templates/protein_design/design_detail.html', {
        'design': design,
        'assays': assays,
    })


def insert_assay(request):
    if request.method == 'POST':
        protocol_form = ProtocolForm(request.POST)
        design_form = DesignForm(request.POST)
        category_form = CategoryForm(request.POST)
        sp_form = SpecificPropertyForm(request.POST)
        unit_form = UnitForm(request.POST)
        bulk_data_form = BulkDataForm(request.POST)

        if (protocol_form.is_valid() and design_form.is_valid() 
                and category_form.is_valid() and sp_form.is_valid() and unit_form.is_valid() and bulk_data_form.is_valid()):

            protocol = protocol_form.save()
            design = design_form.save() 

            category = category_form.save()

            sp = sp_form.save(commit=False)
            sp.fk_id_category = category
            sp.save()

            unit = unit_form.save()
            UnitHasSpecificProperty.objects.create(fk_id_unit=unit, fk_id_sp=sp)

            bulk_text = bulk_data_form.cleaned_data['bulk_data']

            try:
                data_lines = validate_and_parse_bulk_data(bulk_text)
            except ValidationError as e:
                return render(request, 'templates/protein_design/insert_assay.html', {
                    'protocol_form': protocol_form,
                    'design_form': design_form,
                    'category_form': category_form,
                    'sp_form': sp_form,
                    'unit_form': unit_form,
                    'bulk_data_form': bulk_data_form,
                    'error': str(e)
                })

            techniques = {}
            first_technique = None

            for i, (assay_name, sequence, technique_name, result_value, result_type) in enumerate(data_lines):
                if technique_name not in techniques:
                    technique, _ = UsedTechnique.objects.get_or_create(technique_name=technique_name, fk_id_design=design)
                    techniques[technique_name] = technique

                    if i == 0:
                        first_technique = technique
                else:
                    technique = techniques[technique_name]

                assay = Assay.objects.create(
                    assay_name=assay_name,
                    fk_id_protocol=protocol,
                    fk_id_category=category,
                    fk_id_design=design,
                    fk_id_techniques=technique
                )

                Sequence.objects.create(
                    sequence=sequence,
                    fk_id_design=design
                )

                if result_type.lower() == 'computational':
                    ComputationalResult.objects.create(
                        result_value=result_value,
                        fk_id_design=design,
                        fk_id_techniques=technique
                    )
                elif result_type.lower() == 'experimental':
                    ExperimentalResult.objects.create(
                        result_value=result_value,
                        fk_id_design=design,
                        fk_id_techniques=technique
                    )

            return redirect('design_list')

    else:
        protocol_form = ProtocolForm()
        design_form = DesignForm()
        sequence_form = SequenceForm()
        category_form = CategoryForm()
        sp_form = SpecificPropertyForm()
        unit_form = UnitForm()
        assay_form = AssayForm()
        bulk_data_form = BulkDataForm()

    context = {
        'protocol_form': protocol_form,
        'design_form': design_form,
        'sequence_form': sequence_form,
        'category_form': category_form,
        'sp_form': sp_form,
        'unit_form': unit_form,
        'assay_form': assay_form,
        'bulk_data_form': bulk_data_form,
    }

    return render(request, 'templates/protein_design/insert_assay.html', context)

def upload_results(request, design_id, technique_id):
    return HttpResponse(f"Upload results para design {design_id}, técnica {technique_id}")
