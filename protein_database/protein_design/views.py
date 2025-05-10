from django.shortcuts import render, redirect
from django.db import transaction
import csv
import pandas as pd
from django.forms import modelformset_factory
from .filters import AssayFilter
from django.db.models import Prefetch

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
    return render(request, 'design_list.html', {'designs': designs})

#Página de buscas  - /design_search
def design_search(request):
    assay_list = Assay.objects.all()
    assay_filter = AssayFilter(request.GET, queryset=assay_list)
    return render(request, 'design_search.html', {'filter': assay_filter})


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

    return render(request, 'design_detail.html', {
        'design': design,
        'assays': assays,
    })



#adiconar proteina na bd - /add_protein
#def add_protein(request):
#    pass

def insert_assay(request):
    #UsedTechniqueFormSet = modelformset_factory(UsedTechnique, form=UsedTechniqueForm, extra=2, can_delete=False)

    if request.method == 'POST':
        protocol_form = ProtocolForm(request.POST)
        design_form = DesignForm(request.POST)
        sequence_form = SequenceForm(request.POST)
        category_form = CategoryForm(request.POST)
        sp_form = SpecificPropertyForm(request.POST)
        unit_form = UnitForm(request.POST)
        assay_form = AssayForm(request.POST)
        technique_formset = UsedTechniqueFormSet(request.POST, prefix='technique')

        if (protocol_form.is_valid() and design_form.is_valid() and sequence_form.is_valid()
                and category_form.is_valid() and sp_form.is_valid() and unit_form.is_valid()
                and assay_form.is_valid() and technique_formset.is_valid()):

            # salva cada item e guarda as referências para os FKs
            protocol = protocol_form.save()
            design = design_form.save()
            sequence = sequence_form.save(commit=False)
            sequence.fk_id_design = design
            sequence.save()

            category = category_form.save()

            sp = sp_form.save(commit=False)
            sp.fk_id_category = category
            sp.save()

            unit = unit_form.save()

            # relation UnitHasSpecificProperty
            UnitHasSpecificProperty.objects.create(
                fk_id_unit=unit,
                fk_id_sp=sp
            )

            techniques = []
            for form in technique_formset:
                technique = form.save(commit=False)
                technique.fk_id_design = design
                technique.save()
                techniques.append(technique)

            # Assay — assumindo que só haverá uma técnica selecionada no formset para o Assay
            # se quiser que associe todas as técnicas, pode fazer um loop aqui
            if techniques:
                assay = assay_form.save(commit=False)
                assay.fk_id_protocol = protocol
                assay.fk_id_category = category
                assay.fk_id_design = design
                assay.fk_id_techniques = techniques[0]
                assay.save()

            #return redirect('design_list')  # ou outra página de sucesso
            return redirect('upload_results', design_id=design.id_design, technique_id=technique.id_techniques)

    else:
        protocol_form = ProtocolForm()
        design_form = DesignForm()
        sequence_form = SequenceForm()
        category_form = CategoryForm()
        sp_form = SpecificPropertyForm()
        unit_form = UnitForm()
        assay_form = AssayForm()
        technique_formset = UsedTechniqueFormSet(queryset=UsedTechnique.objects.none(), prefix='technique')

    context = {
        'protocol_form': protocol_form,
        'design_form': design_form,
        'sequence_form': sequence_form,
        'category_form': category_form,
        'sp_form': sp_form,
        'unit_form': unit_form,
        'assay_form': assay_form,
        'technique_formset': technique_formset,
    }

    return render(request, 'insert_assay.html', context)

def upload_results(request, design_id, technique_id):
    if request.method == 'POST':
        form = ResultsForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                return render(request, "upload_results.html", {'form': form, 'error': 'Ficheiro inválido'})

            df = pd.read_csv(csv_file, sep=';', encoding='utf-8', header=0)

            expected_columns = ["result_type", "result_value"]
            if not all(col in df.columns for col in expected_columns):
                missing = [col for col in expected_columns if col not in df.columns]
                return render(request, 'upload_results.html', {'form': form, 'error': f'Colunas inválidas: {missing}'})

            for _, row in df.iterrows():
                if row['result_type'].lower() == 'computational':
                    ComputationalResult.objects.create(
                        fk_id_techniques_id=technique_id,
                        fk_id_design_id=design_id,
                        result_value=row['result_value']
                    )
                elif row['result_type'].lower() == 'experimental':
                    ExperimentalResult.objects.create(
                        fk_id_techniques_id=technique_id,
                        fk_id_design_id=design_id,
                        result_value=row['result_value']
                    )
                else:
                    continue

            return redirect('design_list')  # ou outra página de sucesso
    else:
        form = ResultsForm()

    return render(request, 'upload_results.html', {'form': form})

