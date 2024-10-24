from django import forms

# create filter form
class FilterForm(forms.Form):
    query = forms.CharField(required=False, max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search ...'}))
    min_price = forms.DecimalField(
        required=False, min_value=0, decimal_places=2, max_digits=10, widget=forms.TextInput(attrs={'class': 'form-control d-none'}))
    max_price = forms.DecimalField(
        required=False, min_value=0, decimal_places=2, max_digits=10, widget=forms.TextInput(attrs={'class': 'form-control d-none'}))
