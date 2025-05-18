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
    category_name = forms.CharField 
    class Meta:
        model = Category
        fields = ['category_name']
        
    
class SpecificPropertyForm(forms.ModelForm):  #add dropdown in the form
    sp_name = forms.CharField 
    class Meta:
        model = SpecificProperty
        fields = ['sp_name']

class UnitForm(forms.ModelForm):
    unit_name = forms.CharField 
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
    
AssayFormSet = modelformset_factory(
Assay, form=AssayForm, extra=1, can_delete=True)


class BulkDataForm(forms.Form):
    bulk_data = forms.CharField(widget=forms.Textarea, label="(assay_name, sequence, technique_name, result_value, category_name, unit_name, sp_name, result_type)")


class ResultsForm(forms.Form):
    csv_data = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 50}),
        label="Cole os dados do CSV aqui"
    )

    def clean_csv_data(self):
        data = self.cleaned_data['csv_data']
        if not data.strip():
            raise forms.ValidationError("Você deve colar dados CSV.")
        return data

