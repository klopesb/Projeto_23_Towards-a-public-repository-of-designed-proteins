#para adicionar as proteínas na BD a partir da página web 

from django import forms
from django.forms import modelformset_factory
from .models import *

class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ['protocol_name']

class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['design_name', 'pdb_id', 'organism', 'design_type', 'ref_link']

class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ['sequence', 'chain_id', 'length']

class CategoryForm(forms.ModelForm):
    category_name = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        #adicionar dropdown nos forms
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        empty_label="Select a category", 
        required=True
    )

    class Meta:
        model = Category
        fields = ['category_name']

class SpecificPropertyForm(forms.ModelForm):
    class Meta:
        model = SpecificProperty
        fields = ['sp_name']

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_name']

class UsedTechniqueForm(forms.ModelForm):
    class Meta:
        model = UsedTechnique
        fields = ['technique_name', 'technique_type', 'ref_doc']


UsedTechniqueFormSet = modelformset_factory(
    UsedTechnique, form=UsedTechniqueForm, extra=1, can_delete=False
)

class AssayForm(forms.ModelForm):
    class Meta:
        model = Assay
        fields = ['assay_name', 'success_validation']

class ResultsForm(forms.Form):
    #design = forms.ModelChoiceField(queryset=Design.objects.all()) #UsedTechniqueForm #forms.ModelChoiceField(queryset=Design.objects.all())
    #technique = forms.ModelChoiceField(queryset=UsedTechnique.objects.all()) #DesignForm 
    csv_file = forms.FileField()