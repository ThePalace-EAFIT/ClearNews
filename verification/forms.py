from django import forms

class LinkForm(forms.Form):
    url = forms.URLField(label="News Link", widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'https://example.com/news',
    }))
