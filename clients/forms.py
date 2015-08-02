from django import forms
from clients.models import Retailer, Parent


class RetailerForm(forms.ModelForm):

    parent_name = forms.ChoiceField()

    class Meta:
        model = Retailer
        fields = ['parent_name']

    def __init__(self, *args, **kwargs):
        super(RetailerForm, self).__init__(*args, **kwargs)
        parent_choices = [(r.name, r.name) for r in Parent.objects.active_tiers()]
        self.fields['parent_name'].choices = parent_choices
