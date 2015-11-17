from django import forms
from django.core.exceptions import PermissionDenied
from django.db import connection, IntegrityError

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

    def execute(self, user):
        if user is None:
            raise PermissionDenied()

        pk = self.cleaned_data['surprise_id']

        vote, created = models.Vote.objects.get_or_create(
            surprise_id=pk,
            user=user,
            defaults=dict(
                amount=self.increase,
            )
        )

        delta = 0
        if created:
            delta = self.increase
        else:
            delta = -vote.amount
            vote.delete()

        with connection.cursor() as c:
            sql = "update {} set points = points + %s where id = %s".format(
                models.Surprise._meta.db_table,
            )

            c.execute(sql, (delta, pk))


class UpvoteCommand(_VoteCommand):
    increase = 1


class DownvoteCommand(_VoteCommand):
    increase = -1
