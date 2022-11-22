from django import forms
from django.forms import widgets
from webapp.models import Status, Type

class TodoForm(forms.Form):
    short_description = forms.CharField(label='short_description')
    description = forms.CharField(label='description', widget=forms.Textarea())
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='status', widget=widgets.Select)
    type = forms.ModelMultipleChoiceField(required=False, label='type', queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple)



