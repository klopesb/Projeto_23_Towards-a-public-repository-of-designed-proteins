from django.shortcuts import render, redirect
from .filters import AssayFilter
from django.db.models import Prefetch
from .validators import *
from .models import *
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

    # Pegar os IDs únicos de design que aparecem nos ensaios filtrados
    design_ids = assay_filter.qs.values_list('fk_id_design', flat=True).distinct()

    # Buscar os designs correspondentes
    designs = Design.objects.filter(id_design__in=design_ids)

    return render(request, 'templates/protein_design/design_search.html', {
        'filter': assay_filter,
        'designs': designs
    })
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

 # Pega as sequências relacionadas a esse design
    sequences = Sequence.objects.filter(fk_id_design=design)

    return render(request, 'templates/protein_design/design_detail.html', {
        'design': design,
        'assays': assays,
        'sequence_data': sequences
    })


def insert_assay(request):
    if request.method == 'POST':
        protocol_form = ProtocolForm(request.POST)
        design_form = DesignForm(request.POST)
        bulk_data_form = BulkDataForm(request.POST)

        if protocol_form.is_valid() and design_form.is_valid() and bulk_data_form.is_valid():
            protocol = protocol_form.save()
            design = design_form.save()

            bulk_text = bulk_data_form.cleaned_data['bulk_data']

            try:
                data_lines = validate_and_parse_bulk_data(bulk_text)
            except ValidationError as e:
                return render(request, 'templates/protein_design/insert_assay.html', {
                    'protocol_form': protocol_form,
                    'design_form': design_form,
                    'bulk_data_form': bulk_data_form,
                    'error': str(e)
                })

            techniques = {}

            #assay_name;sequence;technique_name;result_value;category;unit;sp;result_type
            for (assay_name, sequence, technique_name, result_value, category_name, unit_name, sp_name, result_type, success_validation) in data_lines:

                # Category
                category, _ = Category.objects.get_or_create(category_name=category_name)

                # Specific Property
                sp, _ = SpecificProperty.objects.get_or_create(sp_name=sp_name, fk_id_category=category)

                # Unit
                unit, _ = Unit.objects.get_or_create(unit_name=unit_name)

                # Relaciona Unit e Specific Property
                UnitHasSpecificProperty.objects.get_or_create(fk_id_unit=unit, fk_id_sp=sp)

                # Technique (caching pra não repetir)
                if technique_name not in techniques:
                    technique, _ = UsedTechnique.objects.get_or_create(
                        technique_name=technique_name,
                        fk_id_design=design
                    )
                    techniques[technique_name] = technique
                else:
                    technique = techniques[technique_name]

                # Assay
                Assay.objects.create(
                    assay_name=assay_name,
                    fk_id_protocol=protocol,
                    fk_id_category=category,
                    fk_id_design=design,
                    fk_id_techniques=technique,
                    success_validation=True if success_validation.lower() in ['true', 'yes', 'y'] else False
                )

                # Sequence
                Sequence.objects.create(
                    sequence=sequence,
                    fk_id_design=design
                )

                # Results
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
        bulk_data_form = BulkDataForm()

    context = {
        'protocol_form': protocol_form,
        'design_form': design_form,
        'bulk_data_form': bulk_data_form,
    }

    return render(request, 'templates/protein_design/insert_assay.html', context)

def upload_results(request, design_id, technique_id):
    return HttpResponse(f"Upload results para design {design_id}, técnica {technique_id}")
