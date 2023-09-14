from django import forms

class WebsiteForm(forms.Form):
    url = forms.URLField(
        label='URL del sitio web',
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: https://www.ejemplo.com'}),
        required=True,
    )
