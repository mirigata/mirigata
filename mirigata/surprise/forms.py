from crispy_forms import helper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Field, Submit, Button, HTML
from django import forms
from . import models


class CreateSurpriseForm(forms.ModelForm):

    class Meta:
        model = models.Surprise
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.layout = Layout(
            Field('link', autofocus=True),
            Field('description', rows=2),

            FormActions(
                Submit('save', 'Create'),
                HTML('<a href="{% url "homepage" %}">Cancel</a>'),
            )
        )

