from django import forms
from django.utils.translation import gettext_lazy as _

class VerificationForm(forms.Form):
    url = forms.URLField(
        required=False,
        label=_("News Link"),
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': _('https://example.com/news'),
        })
    )
    text = forms.CharField(
        required=False,
        label=_("Text"),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'maxlength': '2000',
            'oninput': 'updateCharCount(this)',
            'id': 'news-text',
            'placeholder': _('Or enter the news you want to verify here...'),
    })
)


    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        text = cleaned_data.get('text')

        if not url and not text:
            raise forms.ValidationError(_("You must enter either a URL or some text to verify."))

        if text and len(text) > 2000:
            self.add_error('text', _("Text cannot exceed 2000 characters."))
