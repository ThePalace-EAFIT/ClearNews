from django import forms

class VerificationForm(forms.Form):
    url = forms.URLField(
        required=False,
        label="News Link",
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/news',
        })
    )
    text = forms.CharField(
        required=False,
        label="Text",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'maxlength': '2000',
            'oninput': 'updateCharCount(this)',
            'id': 'news-text',
            'placeholder': 'Or enter the news you want to verify here...',
    })
)


    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        text = cleaned_data.get('text')

        if not url and not text:
            raise forms.ValidationError("You must enter either a URL or some text to verify.")

        if text and len(text) > 2000:
            self.add_error('text', "Text cannot exceed 2000 characters.")
