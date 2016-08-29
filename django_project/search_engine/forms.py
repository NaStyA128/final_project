from django import forms


class SearchForm(forms.Form):
    word = forms.CharField(max_length=100)
