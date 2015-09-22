from crispy_forms import helper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Field, Submit, Button
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
            Field('link', css_class="col-sm-12"),
            Field('description', css_class="col-sm-12", rows=2),

            FormActions(
                Submit('save', 'Create'),
                Button('cancel', 'Cancel'),
            )
        )
