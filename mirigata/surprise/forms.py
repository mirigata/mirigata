from crispy_forms import helper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Field, Submit, HTML
from django import forms

from . import models


class CreateSurpriseCommand(forms.Form):
    link = forms.URLField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.layout = Layout(
            Field('link', autofocus=True),

            FormActions(
                Submit('save', 'Create'),
                HTML('<a href="{% url "homepage" %}">Cancel</a>'),
            )
        )

    def execute(self, user):
        surprise = models.Surprise.objects.create(
            link=self.cleaned_data['link'],
            creator=user,
        )
        models.update_metadata(surprise)

        return surprise
