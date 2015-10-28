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


class _VoteCommand(forms.Form):
    increase = 0
    surprise_id = forms.CharField()

    def execute(self):
        pk = self.cleaned_data['surprise_id']
        surprise = models.Surprise.objects.get(pk=pk)
        surprise.points += self.increase
        surprise.save()
        return surprise


class UpvoteCommand(_VoteCommand):
    increase = 1


class DownvoteCommand(_VoteCommand):
    increase = -1
