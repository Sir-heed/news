from django import forms
from .models import Item
 
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['item_id', 'deleted', 'kids', 'item_time', 'dead', 'kids', 'parent', 'descendants', 'score', 'parent', 'parts', 'editable']


class ItemFilterForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_type']


class SearchForm(forms.Form):
    search = forms.CharField()