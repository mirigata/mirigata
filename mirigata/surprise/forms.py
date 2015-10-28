from django import forms

from . import models
from django.db import connection


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

        with connection.cursor() as c:
            sql = "update {} set points = points + %s where id = %s".format(
                models.Surprise._meta.db_table,
            )

            c.execute(sql, (self.increase, pk))



class UpvoteCommand(_VoteCommand):
    increase = 1


class DownvoteCommand(_VoteCommand):
    increase = -1
