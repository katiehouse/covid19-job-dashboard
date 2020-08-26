from django import forms


class QueryForm(forms.Form):

    zipcode = forms.CharField(label='Location', max_length=100)
    query = forms.CharField(label='Job Title', max_length=100)
