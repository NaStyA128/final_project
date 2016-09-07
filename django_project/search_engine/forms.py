from django import forms


class SearchForm(forms.Form):
    """It form for the searching.

    Attributes:
        keyword: a keyword for the searching.
    """
    keyword = forms.CharField(max_length=100)
