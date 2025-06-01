from django.shortcuts import render, redirect
from .filters import AssayFilter
from django.db.models import Prefetch
from .validators import *
from .models import *
from django.shortcuts import get_object_or_404
from .forms import *
from django.http import HttpResponse
from collections import defaultdict

#Página designs - /designs 
#Fazer uma lista com as proteinas e puxar a imagem do pdb (se der certo)
def design_list(request):
    designs = Design.objects.all()
    return render(request, 'templates/protein_design/design_list.html', {'designs': designs})

#Página de buscas  - /design_search
def design_search(request):
    assay_list = Assay.objects.all()
    assay_filter = AssayFilter(request.GET, queryset=assay_list)

    filtered_assays = assay_filter.qs.distinct() 

    # Pegar os IDs únicos de design que aparecem nos ensaios filtrados
    design_ids = assay_filter.qs.filter(fk_id_design__isnull=False).values_list('fk_id_design', flat=True).distinct()

    # Buscar os designs correspondentes
    designs = Design.objects.filter(id_design__in=design_ids)

    return render(request, 'templates/protein_design/design_search.html', {
        'filter': assay_filter,
        'filtered_assays': filtered_assays, 
        'designs': designs,
    })
#pagina de detalhes do design - /design/<int:id_design>


def design_detail(request, design_id):
    # Recupera o design solicitado ou retorna 404
    design = get_object_or_404(Design, id_design=design_id)

    # Sequências associadas
    sequences = Sequence.objects.filter(fk_id_design=design)

    # Técnicas associadas
    techniques = UsedTechnique.objects.filter(fk_id_design=design)

    # Ensaios associados
    assays = Assay.objects.filter(fk_id_design=design).select_related('fk_id_category')

    # Resultados computacionais associados
    computational_results = ComputationalResult.objects.filter(fk_id_design=design)

    # Resultados experimentais associados
    experimental_results = ExperimentalResult.objects.filter(fk_id_design=design)

    # Units
    units = Unit.objects.all()

    # Categorias para os assays do design
    # (para evitar categorias sem assays, filtramos apenas categorias presentes nos assays)
    categories_ids_in_assays = assays.values_list('fk_id_category__id_category', flat=True).distinct()
    categories = Category.objects.filter(id_category__in=categories_ids_in_assays)

    # Somente as propriedades específicas ligadas ao design via tabela intermediária
    specific_properties = SpecificProperty.objects.filter(
        designhasspecificproperty__fk_id_design=design
    ).select_related('fk_id_category')

    # Agrupando propriedades específicas por categoria, e unidades relacionadas a cada propriedade
    category_data = []
    for category in categories:
        sp_for_category = [sp for sp in specific_properties if sp.fk_id_category == category]
        sp_with_units = []
        for sp in sp_for_category:
            sp_units = Unit.objects.filter(unithasspecificproperty__fk_id_sp=sp)
            sp_with_units.append({
                'property': sp,
                'units': sp_units,
            })
        category_data.append({
            'category': category,
            'specific_properties': sp_with_units,
        })

    context = {
        'design': design,
        'sequences': sequences,
        'techniques': techniques,
        'assays': assays,
        'computational_results': computational_results,
        'experimental_results': experimental_results,
        'units': units,
        'category_data': category_data,
    }

    return render(request, 'templates/protein_design/design_detail.html', context)


def insert_assay(request):
    if request.method == 'POST':
        protocol_form = ProtocolForm(request.POST)
        design_form = DesignForm(request.POST)
        bulk_data_form = BulkDataForm(request.POST)

        if protocol_form.is_valid() and design_form.is_valid() and bulk_data_form.is_valid():
            protocol = protocol_form.save(commit=False)
            design = design_form.save(commit=False)

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
            
            # Save Protocol and Design
            protocol.save()
            design.save()

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
                #UnitHasSpecificProperty.objects.get_or_create(fk_id_unit=unit, fk_id_sp=sp)

                # Relaciona Specific Property e Design
                DesignHasSpecificProperty.objects.get_or_create(fk_id_design=design, fk_id_sp=sp)

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
                seq_obj = Sequence.objects.create(
                    sequence=sequence,
                    fk_id_design=design
                )

                # Results
                if result_type.lower() == 'computational':
                    ComputationalResult.objects.create(
                        result_value=result_value,
                        fk_id_design=design,
                        fk_id_techniques=technique,
                        fk_id_sequence=seq_obj
                    )
                elif result_type.lower() == 'experimental':
                    ExperimentalResult.objects.create(
                        result_value=result_value,
                        fk_id_design=design,
                        fk_id_techniques=technique,
                        fk_id_sequence=seq_obj
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


# def upload_results(request, design_id, technique_id):
#     return HttpResponse(f"Upload results para design {design_id}, técnica {technique_id}")
