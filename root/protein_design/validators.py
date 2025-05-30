from .models import *
from django.core.exceptions import ValidationError

EXPECTED_HEADER = ['assay_name', 'sequence', 'technique_name', 'result_value', 'category_name', 'unit_name', 'sp_name', 'result_type', 'success_validation']


def validate_bulk_header(header_line):
    header = [h.strip().lower() for h in header_line.split(';')]
    if header != EXPECTED_HEADER:
        raise ValidationError(f'Invalid header. Expected: {EXPECTED_HEADER}')
    
    if len(header) != 9:
        raise ValidationError(f'Invalid number of columns ({len(header)}). Expected: 9.')
    
    return header


def validate_bulk_line(line, line_number):

    # Verifica se a linha termina com ';' e gera um erro se for o caso
    if line.strip().endswith(';'):
        raise ValidationError(f'Line {line_number}: Line should not end with a semicolon.')

    parts = [v.strip() for v in line.split(';')]

    if len(parts) != 9:
        raise ValidationError(f'Line {line_number}: Invalid data input ({len(parts)}). Expected: 9  per row.')
    #assay_name;sequence;technique_name;result_value;category;unit;sp;result_type
    assay_name, sequence, technique_name, result_value, category_name, unit_name, sp_name, result_type, success_validation = parts

    if success_validation.lower() not in ['true', 'false']:
        raise ValidationError(f'Line {line_number}: success_validation must be "true" or "false".')

    # Verifica individualmente qual campo está faltando
    missing_fields = []
    if not assay_name:
        missing_fields.append("assay_name")
    if not sequence:
        missing_fields.append("sequence")
    if not technique_name:
        missing_fields.append("technique_name")
    if not result_value:
        missing_fields.append("result_value")
    if not category_name:
        missing_fields.append("category_name")
    if not unit_name:
        missing_fields.append("unit_name")
    if not sp_name:
        missing_fields.append("sp_name")
    if not result_type:
        missing_fields.append("result_type")

    if missing_fields:
        raise ValidationError(f'Line {line_number}: Missing data: {", ".join(missing_fields)}.')

    if result_type.lower() not in ['computational', 'experimental']:
        raise ValidationError(f'Line {line_number}: Invalid result type "{result_type}". Expected: computational or experimental.')

    try:
        float(result_value)
    except ValueError:
        raise ValidationError(f'Line {line_number}: result value "{result_value}" must be numeric or {result_value} is not following the correct format (e.g. 0.1).')

    return parts  # retorna os dados válidos

def validate_and_parse_bulk_data(bulk_text):
    lines = bulk_text.strip().split('\n')
    if len(lines) < 2:
        raise ValidationError('Text must have a header and at least one data line.')

    validate_bulk_header(lines[0])

    data_lines = []
    for i, line in enumerate(lines[1:]):
        if not line.strip():
            continue
        parts = validate_bulk_line(line, i+2)
        data_lines.append(parts)

    if not data_lines:
        raise ValidationError('Any valid data line was found.')

    return data_lines