from django import forms

class LinkForm(forms.Form):
    url = forms.URLField(label="Link de la noticia", widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'https://ejemplo.com/noticia',
    }))
