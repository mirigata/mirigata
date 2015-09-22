from django import forms
from . import models


class CreateSurpriseForm(forms.ModelForm):

    class Meta:
        model = models.Surprise
        exclude = ()
