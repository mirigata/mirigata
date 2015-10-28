from crispy_forms import helper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Field, Submit, HTML
from django import forms

from . import models


class CreateSurpriseCommand(forms.Form):
    link = forms.URLField()

    def execute(self, user):
        surprise = models.Surprise.objects.create(
            link=self.cleaned_data['link'],
            creator=user,
        )
        models.update_metadata(surprise)

        return surprise


class UpvoteCommand(forms.Form):
    surprise_id = forms.CharField()

    def execute(self):
        pk = self.cleaned_data['surprise_id']
        surprise = models.Surprise.objects.get(pk=pk)
        surprise.points += 1
        surprise.save()
        return surprise


class DownvoteCommand(forms.Form):
    surprise_id = forms.CharField()

    def execute(self):
        pk = self.cleaned_data['surprise_id']
        surprise = models.Surprise.objects.get(pk=pk)
        surprise.points -= 1
        surprise.save()
        return surprise
