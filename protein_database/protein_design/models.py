from django.db import models

# Create your models here.


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'categories'


class Design(models.Model):
    id_design = models.AutoField(primary_key=True)
    design_name = models.CharField(max_length=45, null=True, blank=True)
    pdb_id = models.CharField(max_length=45, null=True, blank=True)
    ref_link = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'design'


class Protocol(models.Model):
    id_protocol = models.AutoField(primary_key=True)
    protocol_name = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'protocol'


class UsedTechnique(models.Model):
    id_techniques = models.AutoField(primary_key=True)
    fk_design = models.ForeignKey(Design, on_delete=models.CASCADE)
    technique_name = models.CharField(max_length=45, null=True, blank=True)
    technique_type = models.CharField(max_length=15, choices=[
        ('experimental', 'Experimental'),
        ('computational', 'Computational'),
    ], null=True, blank=True)
    ref_doc = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'used_techniques'
        unique_together = (('id_techniques', 'fk_design'),)


class Assay(models.Model):
    id_assays = models.AutoField(primary_key=True)
    fk_protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    fk_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    fk_design = models.ForeignKey(Design, on_delete=models.CASCADE)
    fk_technique = models.ForeignKey(UsedTechnique, on_delete=models.CASCADE)
    assay_name = models.CharField(max_length=45, null=True, blank=True)
    success_validation = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'assays'
        unique_together = (('id_assays', 'fk_protocol', 'fk_category', 'fk_design', 'fk_technique'),)


class ComputationalResult(models.Model):
    id_computational_results = models.AutoField(primary_key=True)
    fk_technique = models.ForeignKey(UsedTechnique, on_delete=models.CASCADE)
    fk_design = models.ForeignKey(Design, on_delete=models.CASCADE)
    result_file = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = 'computational_results'
        unique_together = (('id_computational_results', 'fk_technique', 'fk_design'),)


class ExperimentalResult(models.Model):
    id_experimental_results = models.AutoField(primary_key=True)
    fk_technique = models.ForeignKey(UsedTechnique, on_delete=models.CASCADE)
    fk_design = models.ForeignKey(Design, on_delete=models.CASCADE)
    result_file = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = 'experimental_results'
        unique_together = (('id_experimental_results', 'fk_technique', 'fk_design'),)


class Sequence(models.Model):
    id_sequences = models.AutoField(primary_key=True)
    fk_design = models.ForeignKey(Design, on_delete=models.CASCADE)
    chain_id = models.CharField(max_length=45, null=True, blank=True)
    sequence = models.TextField(null=True, blank=True)
    length = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'sequences'
        unique_together = (('id_sequences', 'fk_design'),)


class SpecificProperty(models.Model):
    id_sp = models.AutoField(primary_key=True)
    fk_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sp_name = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'specific_property'
        unique_together = (('id_sp', 'fk_category'),)


class Unit(models.Model):
    id_unit = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'unit'


class UnitHasSpecificProperty(models.Model):
    id_unit_sp = models.AutoField(primary_key=True)
    fk_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    fk_sp = models.ForeignKey(SpecificProperty, on_delete=models.CASCADE)

    class Meta:
        db_table = 'unit_has_specific_property'
        unique_together = (('fk_unit', 'fk_sp'),)
