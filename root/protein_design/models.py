from django.db import models

# Create your models here.

class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.category_name or f"Categoria {self.id_category}"

    class Meta:
        db_table = 'categories'

class Design(models.Model):
    id_design = models.AutoField(primary_key=True)
    design_name = models.CharField(max_length=45, null=True, blank=True) #protein name
    pdb_id = models.CharField(max_length=45, null=True, blank=True)
    organism = models.CharField(max_length=45, null=True, blank=True)
    design_type = models.CharField(max_length=45, choices=[
        ('De Novo Design', 'de novo design'),
        ('Protein Engineering', 'protein engineering'),
        ], 
        null=True, blank=True)

    ref_link = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.design_name or f"Design {self.id_design}"

    class Meta:
        db_table = 'design'

class Protocol(models.Model):
    id_protocol = models.AutoField(primary_key=True)
    protocol_name = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.protocol_name or f"Protocol {self.id_protocol}"

    class Meta:
        db_table = 'protocol'


class UsedTechnique(models.Model):
    id_techniques = models.AutoField(primary_key=True)
    fk_id_design = models.ForeignKey(Design, on_delete=models.CASCADE, db_column='fk_id_design')
    technique_name = models.CharField(max_length=45, null=True, blank=True)
    technique_type = models.CharField(max_length=15, choices=[
        ('experimental', 'Experimental'),
        ('computational', 'Computational'),
    ], null=True, blank=True)
    ref_doc = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.technique_name or f"Técnica {self.id_techniques}"

    class Meta:
        db_table = 'used_techniques'
        unique_together = (('id_techniques', 'fk_id_design'),)


class Sequence(models.Model):
    id_sequences = models.AutoField(primary_key=True)
    fk_id_design = models.ForeignKey(Design, on_delete=models.CASCADE, db_column='fk_id_design')
    chain_id = models.CharField(max_length=45, null=True, blank=True)
    sequence = models.TextField(null=True, blank=True)
    length = models.CharField(max_length=45, null=True, blank=True)

    def get_sequence_length(self):
        """Retorna o comprimento da sequência, ignorando espaços e quebras de linha."""
        return len(self.sequence.replace('\n', '').replace(' ', ''))

    class Meta:
        db_table = 'sequences'
        unique_together = (('id_sequences', 'fk_id_design'),)

class Assay(models.Model):
    id_assays = models.AutoField(primary_key=True)
    fk_id_protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, db_column= 'fk_id_protocol' )
    fk_id_category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='fk_id_category')
    fk_id_design = models.ForeignKey(Design, on_delete=models.CASCADE, db_column='fk_id_design')	
    fk_id_techniques = models.ForeignKey(UsedTechnique, on_delete=models.CASCADE, db_column='fk_id_techniques')
    assay_name = models.CharField(max_length=45, null=True, blank=True)
    success_validation = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'assays'
        unique_together = (('id_assays', 'fk_id_protocol', 'fk_id_category', 'fk_id_design', 'fk_id_techniques'),)

class ComputationalResult(models.Model):
    id_computational_results = models.AutoField(primary_key=True)
    fk_id_techniques = models.ForeignKey(UsedTechnique, on_delete=models.CASCADE, db_column='fk_id_techniques')
    fk_id_design = models.ForeignKey(Design, on_delete=models.CASCADE, db_column='fk_id_design')
    fk_id_sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, db_column='fk_id_sequence', null=True, blank=True)
    result_value = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'computational_results'
        unique_together = (('id_computational_results', 'fk_id_techniques', 'fk_id_design', 'fk_id_sequence'),)

class ExperimentalResult(models.Model):
    id_experimental_results = models.AutoField(primary_key=True)
    fk_id_techniques = models.ForeignKey(UsedTechnique, on_delete=models.CASCADE, db_column='fk_id_techniques')
    fk_id_design = models.ForeignKey(Design, on_delete=models.CASCADE, db_column='fk_id_design')
    fk_id_sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, db_column='fk_id_sequence', null=True, blank=True)
    result_file = models.BinaryField(null=True, blank=True)
    result_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'experimental_results'
        unique_together = (('id_experimental_results', 'fk_id_techniques', 'fk_id_design', 'fk_id_sequence'),)


class SpecificProperty(models.Model):
    id_sp = models.AutoField(primary_key=True)
    fk_id_category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='fk_id_category')
    sp_name = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.sp_name or f"Specific Property {self.id_sp}"

    class Meta:
        db_table = 'specific_property'
        unique_together = (('id_sp', 'fk_id_category'),)


class Unit(models.Model):
    id_unit = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.unit_name or f"Unit {self.id_unit}"

    class Meta:
        db_table = 'unit'

class DesignHasSpecificProperty(models.Model):
    fk_id_design = models.ForeignKey(Design, on_delete=models.CASCADE, db_column='fk_id_design')
    fk_id_sp = models.ForeignKey(SpecificProperty, on_delete=models.CASCADE, db_column='fk_id_sp')

    class Meta:
        db_table = 'design_has_specific_property'
        unique_together = (('fk_id_design', 'fk_id_sp'),)
        
class UnitHasSpecificProperty(models.Model):
    fk_id_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, db_column='fk_id_unit', primary_key=True)
    fk_id_sp = models.ForeignKey(SpecificProperty, on_delete=models.CASCADE, db_column='fk_id_sp')

    class Meta:
        db_table = 'unit_has_specific_property'
        unique_together = (('fk_id_unit', 'fk_id_sp'),)  

