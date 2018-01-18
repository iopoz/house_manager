from django import forms


class DateForm(forms.Form):
    before = forms.CharField(label='С:', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ГГГГ-MM-ДД'}))
    after = forms.CharField(label='По:', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ГГГГ-MM-ДД'}))